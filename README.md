# Travel blog articles generation

Generate travel blog articles (in French) using a recurrent neural network.

Runs on CPU or GPU.

## Words-level model

Sample ouput:

> Je suis fatigué du stop qui ne marche pas, et je dois marcher pour la nuit. De toute façon, je vais en profiter pour faire un petit tour de terrain de foot très haut, mais vu que le paysage est en train de dormir dans le désert. Je sais bien que le terrain est à peine pour sortir de la paz, mais je suis dans le vent. La douleur se termine plutôt. Je suis un peu trop faible pour que ça soit normal, et je me fais embarquer en chemin par un groupe de français qui y va en pente. Je ne peux pas dire que sa mort me touche pas, après avoir lu tant de ses amis. Elle est désormais dans le pays, mais pourtant, ça sera à la douane. Bon, maintenant, les choses ne se termine jamais comme prévu, et à un moment, il est possible que les moustiques sont très sympathiques. Ils sont en train de faire du stop tout juste la douane pour ne plus faire par la fenêtre. En fait, elle ne se termine pas, et je les fais à un moment, et je demande au bout de 500 mètres. Je ne compte que trois de leurs enfants sur cinq. Ils sont déjà sur le chemin. Deux heures plus tard, je parcours 50 kilomètres de bas en pente, en me demandant qui va venir me faire payer 50 mètres en direction de la paz. Il y a une station essence et je demande que ça ne va pas être possible. Puis son mari se vide et je leur dit de me laisser là. Et puis, si ils me disent que je ne peux pas dormir, mais tout comme le bus, il me répond. Il me faut un panneau. Après une heure et une heure et une heure et une heure et une heure et un camion à 50 km/h en me faisant des signes de la main, je me fais embarquer par un camion pour 120 km). Vu que je suis en train de faire des informations sur internet, je me fais embarquer par un bus pour un village avec un vieux monsieur à qui je demande si il a eu le sens de cette tente au moment de passer en stop. Il me faut un panneau.

Full sample [here](data/generated/words_sample.txt).

Implemented in [words_model.ipynb](words_model.ipynb), using [fastai code](https://github.com/fastai/fastai/blob/a913af737fbb2e98f89cbcd5ae0e6a8269777859/courses/dl1/lesson4-imdb.ipynb) treated as black-box (but fundamentally a LSTM).

## Chars-level model

Sample output:

> J'ai plus de la montagne n°2, et son propriétaire de la cocaïne, la sortie du Sud et 16 heures et demie de marche. Je lui va pas de ces moments qui ne sont pas de chemins et par exemple, contient pas mal pour le conducteur nous a un lavation de moins de 10 euros de travail de voyage, je suis pas tout est le monde au conducteur se faire concerne. C'est le chemin d'altitude en sait des cacahuètes. Il n'y a pas d'argent pour voir à l'auberge à la sortie d'un camion pour planter la tente, et pas plus de ce moment de la sortie de la capitale de la forêt de la montagne pour un bon moins de l'autostop de marche par un stratégique, c'est la tente. En plus d'altitude est un peu de ces minutes de promenade en même que vous avez la forêt as la montagne est parti de 15 minutes en continuer sur la maison de mon sac à l'expérience, et je ne suis pas rien au contraste au milieu de l'endroit le chemin, vu que je retourne des trucs que j'ai appris à l'auberge pour le contrôle de la route, je fais du camion de commencer des pointilles (et le trafic au conducteur qui commence à au continuer mon propriétaire de la route n°3, et on passe à mon sac de couchage qui collent de la profondeur de manière de l'autostop. Le contrôle de la maison, c'est la tente. Je mange et les camions pour les particuliers a disparu de la tente au camping, c'est la première de la route et son vélo pas de touriste plus maintenant que je suis pas plus de la frontière au conducteur m'embarque.

Full samples: [temperature 0.2](data/generated/chars_sample_0.2.txt), [temperature 0.5](data/generated/chars_sample_0.5.txt), [temperature 0.7](data/generated/chars_sample_0.7.txt).

The higher the temperature, the greater the diversity of words in the sample, at the cost of more spelling mistakes.

Notebook [chars_model.ipynb](chars_model.ipynb) implements successively:
 * A fixed-input-size stateless RNN, from scratch
 * A variable-input-size stateful RNN using `torch.nn.RNN`
 * A stateful 1-layer LSTM, from scratch
 * A stateful 2-layer LSTM using `torch.nn.LSTM`
 * Finally, the model used to generate the above samples: a 3-layers LSTM

## Data

**The data are not open, URLs are hidden purposefully in order to protect the identity of the scrapped blogs.**

The articles of two (french-speaking) travel blogs are downloaded: a blogger (blogspot) blog and a wordpress blog.

The goal is to generate text that looks similar to the blogger blog. Since it is too small a dataset to learn from directly (77k words, 400k characters) the model first learns from a larger wordpress blog (473k words, 2.7M characters).

Retrieving and cleaning the datasets is handled by three scripts:
  * [scrap_wordpress.py](scrap_wordpress.py) downloads the raw blogger HTML articles.
  * [scrap_blogger.py](scrap_blogger.py) downloads the raw wordpress HTML articles.
  * [html_to_txt.py](html_to_txt.py) transforms the raw HTML articles to txt articles. It further discards non-relevant characters (see [analyze_vocab.ipynb](analyze_vocab.ipynb)) and concatenates the result into one txt file.

## Installation notes

`python >= 3.6` is required to run all scripts and notebooks.

### Scrappers

The packages required to run the scrappers (essentially Scrapy and Beautiful Soup) are listed in [requirements.txt](requirements.txt).

### Words-level model

Notebook [words_model.ipynb](words_model.ipynb) requires `fastai v0.7`. See [this thread](https://forums.fast.ai/t/fastai-v0-7-install-issues-thread/24652).

It runs on GPU, but is fairly easy to run on CPU by removing the `.cuda()` mentions in the code.

### Chars-level model

Notebook [chars_model.ipynb](chars_model.ipynb) uses [pytorch 1.0](https://pytorch.org/).

It runs on GPU or CPU, depending on the content of the `GPU` flag declared on top of the notebook.
