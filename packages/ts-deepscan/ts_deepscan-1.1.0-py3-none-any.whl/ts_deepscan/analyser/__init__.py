# SPDX-FileCopyrightText: 2020 EACG GmbH
#
# SPDX-License-Identifier: Apache-2.0

from typing import List

from .Dataset import Dataset

from .FileAnalyser import FileAnalyser
from .SourcesAnalyser import SourcesAnalyser
from .LicenseAnalyser import LicenseAnalyser

from ..config import get_datasetdir

def get_default_analysers() -> List[FileAnalyser]:
    import spacy

    path = get_datasetdir()
    dataset = Dataset(path)

    if not spacy.util.is_package('en_core_web_sm'):
        spacy.cli.download('en_core_web_sm')
        print()

    if not spacy.util.is_package('en_core_web_sm'):
        print('Cannot download language model')
        exit(2)

    print('Loading dataset...')
    dataset.load()

    return [LicenseAnalyser(dataset), SourcesAnalyser(dataset)]