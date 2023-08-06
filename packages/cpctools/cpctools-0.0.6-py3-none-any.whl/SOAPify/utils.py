import numpy
from ase.data import atomic_numbers
from itertools import combinations_with_replacement


def _SOAPpstr(l, Z, n, Zp, np) -> str:
    if atomic_numbers[Z] < atomic_numbers[Zp]:
        Z, Zp = Zp, Z
        n, np = np, n
    return f"{l}_{Z}{n}_{Zp}{np}"


def getdscribeSOAPMapping(
    lmax: int, nmax: int, species: "list[str]", crossover: bool = True
) -> numpy.ndarray:
    """return a list of string with the identities of the data returned from dscribe,
       see the note in https://singroup.github.io/dscribe/1.2.x/tutorials/descriptors/soap.html

    Args:
        lmax (int): the lmax specified in the calculation.
        nmax (int): the nmax specified in the calculation.
        species (list[str]): the list of atomic species.
        crossover (bool): if True, the SOAP descriptors are generated for the mixed species

    Returns:
        numpy.ndarray: an array of strings with the mapping of the output of the analysis
    """
    species = orderByZ(species)
    pdscribe = []
    for Z in species:
        for Zp in species:
            if not crossover and Z != Zp:
                continue
            for l in range(lmax + 1):
                for n in range(nmax):
                    for np in range(nmax):
                        if (np, atomic_numbers[Zp]) >= (n, atomic_numbers[Z]):
                            pdscribe.append(_SOAPpstr(l, Z, n, Zp, np))
    return numpy.array(pdscribe)


def _getRSindex(nmax: int, species: "list[str]") -> numpy.ndarray:
    """Support function for quippy"""
    rs_index = numpy.zeros((2, nmax * len(species)), dtype=numpy.int32)
    i = 0
    for i_species in range(len(species)):
        for na in range(nmax):
            rs_index[:, i] = na, i_species
            i += 1
    return rs_index


def getquippySOAPMapping(
    lmax: int, nmax: int, species: "list[str]", diagonalRadial: bool = False
) -> numpy.ndarray:
    """return a list of string with the identities of the data returned from quippy,
       see https://github.com/libAtoms/GAP/blob/main/descriptors.f95#L7588

    Args:
        lmax (int): the lmax specified in the calculation.
        nmax (int): the nmax specified in the calculation.
        species (list[str]): the list of atomic species.
        diagonalRadial (bool): if True, Only return the n1=n2 elements of the power spectrum. *NOT IMPLEMENTED*


    Returns:
        numpy.ndarray: an array of strings with the mapping of the output of the analysis
    """
    species = orderByZ(species)
    rs_index = _getRSindex(nmax, species)
    pquippy = []
    for ia in range(len(species) * nmax):
        np = rs_index[0, ia]
        Zp = species[rs_index[1, ia]]
        for jb in range(ia + 1):  # ia is  in the range
            n = rs_index[0, jb]
            Z = species[rs_index[1, jb]]
            # if diagonalRadial and np != n:
            #    continue

            for l in range(lmax + 1):
                pquippy.append(_SOAPpstr(l, Z, n, Zp, np))
    return numpy.array(pquippy)


def orderByZ(species: "list[str]") -> "list[str]":
    """Orders the list of species by their atomic number

    Args:
        species (list[str]): the list of atomic species to be ordered

    Returns:
        list[str]: the ordered list of atomic species
    """
    return sorted(species, key=lambda x: atomic_numbers[x])


def getAddressesQuippyLikeDscribe(
    lmax: int, nmax: int, species: "list[str]"
) -> numpy.ndarray:
    """Given the lmax and nmax of a SOAP calculation and the species of the atoms returns an array of idexes for reordering the quippy results as the dscribe results

    Args:
        lmax (int): the lmax specified in the calculation.
        nmax (int): the nmax specified in the calculation.
        species (list[str]): the list of atomic species.

        Returns:
            numpy.ndarray: an array of indexes
    """
    species = orderByZ(species)
    nsp = len(species)
    addresses = numpy.zeros(
        (lmax + 1) * ((nmax * nsp) * (nmax * nsp + 1)) // 2, dtype=int
    )
    quippyOrder = getquippySOAPMapping(lmax, nmax, species)
    dscribeOrder = getdscribeSOAPMapping(lmax, nmax, species)
    for i, s in enumerate(addresses):
        addresses[i] = numpy.where(quippyOrder == dscribeOrder[i])[0][0]
    return addresses


def normalizeArray(a: numpy.ndarray) -> numpy.ndarray:
    """Normalizes the futher axis of the given array

    (eg. in an array of shape (100,50,3) normalizes all the  5000 3D vectors)

    Args:
        a (numpy.ndarray): the arra to be normalized

    Returns:
        numpy.ndarray: the normalized array
    """
    norm = numpy.linalg.norm(a, axis=-1, keepdims=True)
    norm[norm == 0] = 1
    return a / norm


def getSlicesFromAttrs(attrs: dict) -> "tuple(list,dict)":
    """Given the attributes of from a SOAP dataset returns the slices of the SOAP vector that contains the pair information

    Args:
        attrs (dict): the attributes of the SOAP dataset

    Returns:
        tuple(list,dict): the slices of the SOAP vector to be extracted and the atomic types
    """
    species = attrs["species"]
    slices = {}
    for s1 in species:
        for s2 in species:
            if (f"species_location_{s1}-{s2}") in attrs:
                slices[s1 + s2] = slice(
                    attrs[f"species_location_{s1}-{s2}"][0],
                    attrs[f"species_location_{s1}-{s2}"][1],
                )

    return species, slices


def _getIndexesForFillSOAPVectorFromdscribeSapeSpecies(
    l_max: int,
    n_max: int,
) -> numpy.ndarray:
    """given l_max and n_max returns the indexes of the SOAP vector to be reordered to filla  complete vector
    useful to calculate the correct distances between the SOAP vectors

    Args:
        l_max (int): the lmax specified in the calculation.
        n_max (int): the nmax specified in the calculation.

    Returns:
        numpy.ndarray: the array of the indexes in the correct order
    """

    completeData = numpy.zeros(((l_max + 1), n_max, n_max), dtype=int)
    limitedID = 0
    for l in range(l_max + 1):
        for n in range(n_max):
            for np in range(n, n_max):
                completeData[l, n, np] = limitedID
                completeData[l, np, n] = limitedID
                limitedID += 1
    return completeData.reshape(-1)


def _getIndexesForFillSOAPVectorFromdscribe(
    l_max: int,
    n_max: int,
    atomTypes: list = [None],
    atomicSlices: dict = None,
) -> numpy.ndarray:
    """Given the data of a SOAP calculation from dscribe returns the SOAP power
        spectrum with also the symmetric part explicitly stored, see the note in https://singroup.github.io/dscribe/1.2.x/tutorials/descriptors/soap.html

        No controls are implemented on the shape of the soapFromdscribe vector.

    Args:
        soapFromdscribe (numpy.ndarray): the result of the SOAP calculation from the dscribe utility
        l_max (int): the l_max specified in the calculation. Defaults to 8.
        n_max (int): the n_max specified in the calculation. Defaults to 8.
        atomTypes (list[str]): the list of atomic species. Defaults to [None].
        atomicSlices (dict): the slices of the SOAP vector relative to che atomic species combinations. Defaults to None.

    Returns:
        numpy.ndarray: The full soap spectrum, with the symmetric part sored explicitly
    """
    if atomTypes == [None]:
        return _getIndexesForFillSOAPVectorFromdscribeSapeSpecies(l_max, n_max)
    else:
        nOfFeatures = (l_max + 1) * n_max * n_max
        nofCombinations = len(list(combinations_with_replacement(atomTypes, 2)))
        completeData = numpy.zeros(nOfFeatures * nofCombinations, dtype=int)
        combinationID = 0
        for i, s1 in enumerate(atomTypes):
            for j in range(i, len(atomTypes)):
                s2 = atomTypes[j]
                completeID = combinationID * nOfFeatures
                completeSlice = slice(
                    completeID,
                    completeID + nOfFeatures,
                )
                if s1 == s2:
                    completeData[completeSlice] = (
                        _getIndexesForFillSOAPVectorFromdscribeSapeSpecies(l_max, n_max)
                        + atomicSlices[s1 + s2].start
                    )
                else:
                    completeData[completeSlice] = (
                        numpy.arange(nOfFeatures, dtype=int)
                        + atomicSlices[s1 + s2].start
                    )
                combinationID += 1
        return completeData


def fillSOAPVectorFromdscribe(
    soapFromdscribe: numpy.ndarray,
    l_max: int,
    n_max: int,
    atomTypes: list = [None],
    atomicSlices: dict = None,
) -> numpy.ndarray:
    """Given the result of a SOAP calculation from dscribe returns the SOAP power spectrum
        with also the symmetric part explicitly stored, see the note in https://singroup.github.io/dscribe/1.2.x/tutorials/descriptors/soap.html

        No controls are implemented on the shape of the soapFromdscribe vector.

    Args:
        soapFromdscribe (numpy.ndarray): the result of the SOAP calculation from the dscribe utility
        l_max (int): the l_max specified in the calculation.
        n_max (int): the n_max specified in the calculation.

    Returns:
        numpy.ndarray: The full soap spectrum, with the symmetric part sored explicitly
    """
    upperDiag = int((l_max + 1) * (n_max) * (n_max + 1) / 2)
    fullmat = n_max * n_max * (l_max + 1)
    limitedSOAPdim = upperDiag * len(atomTypes) + fullmat * int(
        (len(atomTypes) - 1) * len(atomTypes) / 2
    )
    # enforcing the order of the atomTypes
    if len(atomTypes) > 1:
        atomTypes = list(atomTypes)
        atomTypes.sort(key=lambda x: atomic_numbers[x])

    if soapFromdscribe.shape[-1] != limitedSOAPdim:
        raise Exception(
            "fillSOAPVectorFromdscribe: the given soap vector do not have the expected dimensions"
        )
    indexes = _getIndexesForFillSOAPVectorFromdscribe(
        l_max, n_max, atomTypes, atomicSlices
    )
    if len(soapFromdscribe.shape) == 1:
        return soapFromdscribe[indexes]
    elif len(soapFromdscribe.shape) == 2:
        return soapFromdscribe[:, indexes]
    elif len(soapFromdscribe.shape) == 3:
        return soapFromdscribe[:, :, indexes]
    else:
        raise Exception(
            "fillSOAPVectorFromdscribe: cannot convert array with len(shape) >=3"
        )
