# wordle-operator

Play Wordle from any Kubernetes cluster.

## Manual setup steps

```
docker build . -t lucasmelin/wordle-operator
kubectl create namespace wordle
kubectl apply -f wordle-operator.yaml -n wordle
kubectl api-resources # Shows the new resource
kubectl apply -f guess.yaml -n wordle # Make a guess
kubectl get configmaps -n wordle # Look at the results
kubectl describe configmaps wordle-<id> -n wordle
# Change the word in guess.yaml
kubectl apply -f guess.yaml -n wordle # Make another guess
```

## Uninstall
```bash
kubectl delete crd wordles.operators.lucasmelin.com