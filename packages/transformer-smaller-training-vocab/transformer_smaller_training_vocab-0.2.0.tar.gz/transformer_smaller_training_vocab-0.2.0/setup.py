# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transformer_smaller_training_vocab',
 'transformer_smaller_training_vocab.transformer_set_vocab']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.0.0,<3.0.0',
 'sentencepiece>=0.1.97,<0.2.0',
 'torch>=1.8.0,<2.0.0',
 'transformers[torch]>=4.1,<5.0']

setup_kwargs = {
    'name': 'transformer-smaller-training-vocab',
    'version': '0.2.0',
    'description': 'Temporary remove unused tokens during training to save ram and speed.',
    'long_description': '# transformer-smaller-training-vocab\n\n[![PyPI version](https://badge.fury.io/py/transformer-smaller-training-vocab.svg)](https://badge.fury.io/py/transformer-smaller-training-vocab)\n[![GitHub Issues](https://img.shields.io/github/issues/helpmefindaname/transformer-smaller-training-vocab.svg)](https://github.com/helpmefindaname/transformer-smaller-training-vocab/issues)\n[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)\n\n## Motivation\n\nHave you ever trained a transformer model and noticed that most tokens in the vocab are not used?\nLogically the token embeddings from those terms won\'t change, however they still take up memory and compute resources on your GPU.\nOne could assume that the embeddings are just a small part of the model and therefore aren\'t relevant, however looking at models like [xlm-roberta-large](https://huggingface.co/xlm-roberta-large) have 45.72% of parameters as "word_embeddings".\nBesides that, the gradient computation is done for the whole embedding weight, leading to gradient updates with very large amounts of 0s, eating a lot of memory, especially with state optimizers such as adam.\n\nTo reduce these inconveniences, this package provides a simple and easy to use way to\n* gather usage statistics of the vocabulary\n* temporary reduce the vocabulary to include no tokens that won\'t be used during training\n* fit in the tokens back in after the training is finished, so the full version can be saved.\n\n\n### Limitations\n\nThis library works fine, if you use any [FastTokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer#transformers.PreTrainedTokenizerFast)\nHowever if you want to use a `slow` tokenizer, it get\'s more tricky as huggingface-transformers has - per current date - no interface for overwriting the vocabulary in transformers.\nSo they require a custom implementation, currently the following tokenizers are supported:\n* XLMRobertaTokenizer\n* RobertaTokenizer\n* BertTokenizer\n\nIf you want to use a tokenizer that is not on the list, please [create an issue](https://github.com/helpmefindaname/transformer-smaller-training-vocab/issues) for it.\n\n## Quick Start\n\n### Requirements and Installation\n\nThe project is based on Transformers 4.1.0+, PyTorch 1.8+ and Python 3.7+\nThen, in your favorite virtual environment, simply run:\n\n```\npip install transformer-smaller-training-vocab\n```\n\n### Example Usage\n\nTo use more efficient training, it is enough to do the following changes to an abitary training script:\n\n```diff\n\n  model = ...\n  tokenizer = ...\n  raw_datasets = ...\n  ...\n\n+ with reduce_train_vocab(model=model, tokenizer=tokenizer, texts=get_texts_from_dataset(raw_datasets, key="text")):\n      def preprocess_function(examples):\n          result = tokenizer(examples["text"], padding=padding, max_length=max_seq_length, truncation=True)\n          result["label"] = [(label_to_id[l] if l != -1 else -1) for l in examples["label"]]\n          return result\n    \n      raw_datasets = raw_datasets.map(\n          preprocess_function,\n          batched=True,\n      )\n    \n      trainer = Trainer(\n          model=model,\n          train_dataset=raw_datasets["train"],\n          eval_dataset=raw_datasets["validation"],\n          tokenizer=tokenizer,\n          ...\n      )\n    \n      trainer.train()\n\n+ trainer.save_model()  # save model at the end to contain the full vocab again.\n```\n\nDone! The Model will now be trained with only use the necessary parts of the token embeddings.\n\n## Impact\n\nHere is a table to document how much impact this technique has on training:\n\n| **Model** | **Dataset** | **Vocab reduction** | **Model size reduction** |\n|-----------|-------------|---------------------|--------------------------|\n| [xlm-roberta-large](https://huggingface.co/xlm-roberta-large) | CONLL 03 (en) |  93.13% | 42.58% |\n| [xlm-roberta-base](https://huggingface.co/xlm-roberta-base) | CONLL 03 (en) | 93.13% | 64.31% |\n| [bert-base-cased](https://huggingface.co/bert-base-cased) | CONLL 03 (en) | 43.64% | 08.97% |\n| [bert-base-uncased](https://huggingface.co/bert-base-uncased) | CONLL 03 (en) | 47.62% | 10.19% |\n| [bert-large-uncased](https://huggingface.co/roberta-base) | CONLL 03 (en) | 47.62% | 04.44% |\n| [roberta-base](https://huggingface.co/roberta-base) | CONLL 03 (en) | 58.39% | 18.08% |\n| [roberta-large](https://huggingface.co/roberta-large) | CONLL 03 (en) | 58.39% | 08.45% |\n\nNotice that while those reduced embeddings imply slightly less computation effort, those gains are neglectable, as the gradient computation for the parameters of transformer layers are dominant.\n',
    'author': 'Benedikt Fuchs',
    'author_email': 'benedikt.fuchs.staw@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/helpmefindaname/transformer-smaller-training-vocab',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
