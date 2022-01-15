# wordle-operator 🟩⬛🟩🟨⬛

Play Wordle from any Kubernetes cluster.

---

Using the power of CustomResourceDefinitions and Kubernetes Operators, now you can play [Wordle](https://www.powerlanguage.co.uk/wordle/), the game by [Josh Wardle](https://twitter.com/powerlanguish), in your Kubernetes cluster.

[![asciicast](https://asciinema.org/a/fMFpFak5lAMIa9qabmIeyuY0C.svg)](https://asciinema.org/a/fMFpFak5lAMIa9qabmIeyuY0C)

## Installation

```bash
# Copy wordle-operator.yaml locally
kubectl create namespace wordle
kubectl apply -f wordle-operator.yaml -n wordle
kubectl api-resources --api-group='operators.lucasmelin.com' # Shows the new resource
```

<details>
  <summary>Alternative - Build and install from source</summary>

## Build and install from source
```bash
# Setup
git clone https://github.com/lucasmelin/wordle-operator.git
cd wordle-operator
docker build . -t lucasmelin/wordle-operator
kubectl create namespace wordle
kubectl apply -f wordle-operator.yaml -n wordle
kubectl api-resources --api-group='operators.lucasmelin.com' # Shows the new resource
```

</details>


## Playing the game

```bash
# Start guessing - use guess.yaml as a reference for the format
kubectl apply -f guess.yaml -n wordle # Make a guess
kubectl describe configmaps -n wordle # Look at the result of your guess

# Change the word to your new guess in guess.yaml
kubectl apply -f guess.yaml -n wordle # Make another guess
kubectl describe configmaps -n wordle # Look at the result of your guess
```

## Uninstall
```bash
kubectl delete crd wordles.operators.lucasmelin.com
kubectl delete namespace wordle
```