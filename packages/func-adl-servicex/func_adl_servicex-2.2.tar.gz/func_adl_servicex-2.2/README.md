# func_adl_servicex

Send func_adl expressions to a ServiceX endpoint

[![GitHub Actions Status](https://github.com/iris-hep/func_adl_servicex/workflows/CI/CD/badge.svg)](https://github.com/iris-hep/func_adl_servicex/actions)
[![Code Coverage](https://codecov.io/gh/iris-hep/func_adl_servicex/graph/badge.svg)](https://codecov.io/gh/iris-hep/func_adl_servicex)

[![PyPI version](https://badge.fury.io/py/func-adl-servicex.svg)](https://badge.fury.io/py/func-adl-servicex)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/func-adl-servicex.svg)](https://pypi.org/project/func-adl-servicex/)

## Introduction

This package contains the single object `ServiceXSourceXAOD` and `ServiceXSourceUpROOT` which can be used as a root of a `func_adl` expression to query large LHC datasets from an active `ServiceX` instance located on the net.

See below for simple examples.

### Further Information

- `servicex` documentation
- `func_adl` documentation

## Usage

To use `func_adl` on `servicex`, the only `func_adl` package you need to install this package. All others required will be pulled in as dependencies of this package.

## Using the xAOD backend

See the further information for documentation above to understand how this works. Here is a quick sample that will run against an ATLAS `xAOD` backend in `servicex` to get out jet pt's for those jets with `pt > 30` GeV.

```python
from func_adl_servicex import ServiceXSourceXAOD

dataset_xaod = "mc15_13TeV:mc15_13TeV.361106.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zee.merge.DAOD_STDM3.e3601_s2576_s2132_r6630_r6264_p2363_tid05630052_00"
ds = ServiceXSourceXAOD(dataset_xaod)
data = (
    ds
    .SelectMany('lambda e: (e.Jets("AntiKt4EMTopoJets"))')
    .Where('lambda j: (j.pt()/1000)>30')
    .Select('lambda j: j.pt()')
    .AsAwkwardArray(["JetPt"])
    .value()
)

print(data['JetPt'])
```

## Using the CMS Run 1 AOD backend

See the further information for documentation above to understand how this works. Here is a quick sample that will run against an CMS Run 1 `AOD` backend in `servicex`. It turns against a 6 TB CMS Open Data dataset, selecting global muons with a pT greater than 30 GeV.

```python
from func_adl_servicex import ServiceXSourceCMSRun1AOD

dataset_xaod = "cernopendata://16"
ds = ServiceXSourceCMSRun1AOD(dataset_xaod)
data = (
    ds
    .SelectMany(lambda e: e.TrackMuons("globalMuons"))
    .Where(lambda m: m.pt() > 30)
    .Select(lambda m: m.pt())
    .AsAwkwardArray(['mu_pt'])
    .value()
)

print(data['mu_pt'])
```

## Using the uproot backend

See the further information for documentation above to understand how this works. Here is a quick sample that will run against a ROOT file (TTree) in the `uproot` backend in `servicex` to get out jet pt's. Note that the image name tag is likely wrong here. See XXX to get the current one.

```python
from servicex import ServiceXDataset
from func_adl_servicex import ServiceXSourceUpROOT


dataset_uproot = "user.kchoi:user.kchoi.ttHML_80fb_ttbar"
uproot_transformer_image = "sslhep/servicex_func_adl_uproot_transformer:issue6"

sx_dataset = ServiceXDataset(dataset_uproot, image=uproot_transformer_image)
ds = ServiceXSourceUpROOT(sx_dataset, "nominal")
data = (
    ds.Select("lambda e: {
        'lep_pt_1': e.lep_Pt_1,
        'lep_pt_2': e.lep_Pt_2
        }")
    .value()

print(data)
```

## Running on Local Datasets

It is possible to run on local files. This works well when testing or building out your code, but is horrible if you need to run on a large number of files. It is recommended to use this only with a single file. It is, for the most part, a drop-in replacement for the `ServiceX` backend version.

First, you must install the `local` variant of `func_adl_servicex`. If you are using `pip`, you can do the following:

```bash
pip install func_adl_servicex[local]
```

With that installed, the following will work:

```python
from func_adl_servicex import SXLocalxAOD

dataset_xaod = "my_local_xaod.root"
ds = SXLocalxAOD(dataset_xaod)
data = (ds
    .SelectMany('lambda e: (e.Jets("AntiKt4EMTopoJets"))')
    .Where('lambda j: (j.pt()/1000)>30')
    .Select('lambda j: j.pt()')
    .AsAwkwardArray(["JetPt"])
    .value()
)

print(data['JetPt'])
```

And replace `SXLocalxAOD` with `SXLocalCMSRun1AOD` for using CMS backend (and, of course, update the query).

## Development

PR's are welcome! Feel free to add an issue for new features or questions.

The `master` branch is the most recent commits that both pass all tests and are slated for the next release. Releases are tagged. Modifications to any released versions are made off those tags.

## Qastle

This is for people working with the back-ends that run in `servicex`.

This is the `qastle` produced for an xAOD dataset:

```text
(call EventDataset 'ServiceXDatasetSource')
```

(the actual dataset name is passed in the `servicex` web API call.)

This is the `qastle` produced for a ROOT flat file:

```text
(call EventDataset 'ServiceXDatasetSource' 'tree_name')
```
