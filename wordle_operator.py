#!/usr/bin/env python3

from typing import List
import kopf
from calculate_word import todays_word
from wordlist import valid, words
import kubernetes.client as k8s_client
import kubernetes.config as k8s_config

status = ["Genius", "Magnificent", "Impressive", "Splendid", "Great", "Phew"]


wordle_crd = k8s_client.V1CustomResourceDefinition(
    api_version="apiextensions.k8s.io/v1",
    kind="CustomResourceDefinition",
    metadata=k8s_client.V1ObjectMeta(name="wordles.operators.lucasmelin.com"),
    spec=k8s_client.V1CustomResourceDefinitionSpec(
        group="operators.lucasmelin.com",
        versions=[
            k8s_client.V1CustomResourceDefinitionVersion(
                name="v1",
                served=True,
                storage=True,
                schema=k8s_client.V1CustomResourceValidation(
                    open_apiv3_schema=k8s_client.V1JSONSchemaProps(
                        type="object",
                        properties={
                            "spec": k8s_client.V1JSONSchemaProps(
                                type="object",
                                properties={
                                    "guess": k8s_client.V1JSONSchemaProps(
                                        type="string",
                                        description="The word to guess",
                                    )
                                },
                            ),"status": k8s_client.V1JSONSchemaProps(
                            type="object",
                            x_kubernetes_preserve_unknown_fields=True
                        )
                        },
                    )
                ),
            )
        ],
        scope="Namespaced",
        names=k8s_client.V1CustomResourceDefinitionNames(
            plural="wordles",
            singular="wordle",
            kind="Wordle",
            short_names=["wd"],
        ),
    ),
)
try:
    k8s_config.load_kube_config()
except k8s_config.ConfigException:
    k8s_config.load_incluster_config()

api_instance = k8s_client.ApiextensionsV1Api()
try:
    api_instance.create_custom_resource_definition(wordle_crd)
except k8s_client.rest.ApiException as e:
    if e.status == 409:
        print("Custom Resource Definition already exists")
    else:
        raise e


@kopf.on.create("operators.lucasmelin.com", "v1", "wordles")
def on_create(namespace, spec, body, **kwargs):
    guess = spec["guess"]
    if guess in words + valid:
        guess_result = test_guess(guess)
    else:
        guess = f"The guess {guess} is not in the word list"
        guess_result = [0, 0, 0, 0, 0]
    data = __guess_config_map_data(guess, guess_result)
    kopf.adopt(data)
    config_map = create_guess_config_map(namespace, data)
    return {"configmap-name": config_map.metadata.name}


@kopf.on.update("operators.lucasmelin.com", "v1", "wordles")
def on_update(namespace, name, spec, status, **kwargs):
    guess = spec["guess"]
    if guess in words + valid:
        guess_result = test_guess(guess)
    else:
        guess = f"The guess {guess} is not in the word list"
        guess_result = [0, 0, 0, 0, 0]
    name = status["on_create"]["configmap-name"]
    data = __guess_config_map_data(guess, guess_result)
    update_guess_config_map(namespace, name, data)


def create_guess_config_map(namespace, data):
    client = k8s_client.CoreV1Api()
    return client.create_namespaced_config_map(namespace, data)


def update_guess_config_map(namespace, name, new_data):
    client = k8s_client.CoreV1Api()
    return client.patch_namespaced_config_map(
        namespace=namespace, name=name, body=new_data
    )


def __guess_config_map_data(guess, guess_result):
    emoji_result = ""
    for i in guess_result:
        if i == 2:
            emoji_result += "🟩"
        elif i == 1:
            emoji_result += "🟨"
        else:
            emoji_result += "⬛"
    return {"data": {"guess": guess, "result": emoji_result}}


def test_guess(guess) -> List:
    """Return the accuracy of the guess."""
    actual_word = todays_word()
    guess_result = [0, 0, 0, 0, 0]
    for idx, letter in enumerate(guess):
        if letter == actual_word[idx]:
            guess_result[idx] = 2
            actual_word = blank_letter(actual_word, index=idx)
    for idx, letter in enumerate(guess):
        if letter in actual_word:
            guess_result[idx] = 1
            actual_word = blank_letter(actual_word, letter=letter)
    return guess_result


def blank_letter(word, index=None, letter=None):
    if index is not None:  # 0 is falsy
        return word[:index] + "_" + word[index + 1 :]
    elif letter:
        return word.replace(letter, "_", 1)
    else:
        return word
