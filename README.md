# FaaS Latency Benchmark

Benchmark comparing Azure Functions vs OpenFaaS by deploying an identical heap-sort HTTP
function on both platforms and measuring end-to-end latency.

## Structure

- `azure/` — Azure Functions app (`function_app.py`)
- `openfaas/` — OpenFaaS stack + `hello-python` handler
- `azureFaaStest.py` — benchmark harness (cold/warm start, heavy/easy computation, input-length sweeps)
- `graphMaking.ipynb` — result analysis and plots
- `results/` — raw CSVs from Azure and OpenFaaS runs
- `figures/` — generated plots

## Running the benchmark

1. Deploy the function on Azure (`func azure functionapp publish ...`) and/or OpenFaaS.
2. Set the function `URL` at the top of `azureFaaStest.py`.
3. Uncomment the desired scenario and run: `python azureFaaStest.py`

