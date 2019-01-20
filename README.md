# Travel blog articles generation

Generate (french) travel blog articles with recurrent neural network.

## Words-level model

Sample ouput:

> Je suis fatigué du stop qui ne marche pas, et je dois marcher pour la nuit. De toute façon, je vais en profiter pour faire un petit tour de terrain de foot très haut, mais vu que le paysage est en train de dormir dans le désert. Je sais bien que le terrain est à peine pour sortir de la paz, mais je suis dans le vent. La douleur se termine plutôt. Je suis un peu trop faible pour que ça soit normal, et je me fais embarquer en chemin par un groupe de français qui y va en pente. Je ne peux pas dire que sa mort me touche pas, après avoir lu tant de ses amis. Elle est désormais dans le pays, mais pourtant, ça sera à la douane. Bon, maintenant, les choses ne se termine jamais comme prévu, et à un moment, il est possible que les moustiques sont très sympathiques. Ils sont en train de faire du stop tout juste la douane pour ne plus faire par la fenêtre. En fait, elle ne se termine pas, et je les fais à un moment, et je demande au bout de 500 mètres. Je ne compte que trois de leurs enfants sur cinq. Ils sont déjà sur le chemin. Deux heures plus tard, je parcours 50 kilomètres de bas en pente, en me demandant qui va venir me faire payer 50 mètres en direction de la paz. Il y a une station essence et je demande que ça ne va pas être possible. Puis son mari se vide et je leur dit de me laisser là. Et puis, si ils me disent que je ne peux pas dormir, mais tout comme le bus, il me répond. Il me faut un panneau. Après une heure et une heure et une heure et une heure et une heure et un camion à 50 km/h en me faisant des signes de la main, je me fais embarquer par un camion pour 120 km). Vu que je suis en train de faire des informations sur internet, je me fais embarquer par un bus pour un village avec un vieux monsieur à qui je demande si il a eu le sens de cette tente au moment de passer en stop. Il me faut un panneau.

Full sample [here](data/generated/words_sample.txt).

Implemented in [words_model.ipynb], using [fastai code](https://github.com/fastai/fastai/blob/a913af737fbb2e98f89cbcd5ae0e6a8269777859/courses/dl1/lesson4-imdb.ipynb) treated as black-box (but fundamentally a LSTM).

## Data

**The data are not open, URLs are hidden purposefully in order to protect the identity of the scrapped blogs.**

The articles of two (french-speaking) travel blogs are downloaded: a blogger (blogspot) blog and a wordpress blog.

The goal is to generate text that looks similar to the blogger blog. Since it is too small a dataset to learn from directly (77k words, 400k characters) we'll learn from a larger wordpress blog first (473k words, 2.7M characters).

Retrieving and cleaning the datasets is handled by three scripts:
  * [scrap_wordpress.py] downloads the raw blogger HTML articles.
  * [scrap_blogger.py] downloads the raw wordpress HTML articles.
  * [html_to_txt.py] transforms the raw HTML articles to txt articles. It further discards non-relevant characters (see [analyze_vocab.ipynb]) and concatenates the result into one txt file.

## Installation notes

The words-level notebook ([words_model.ipynb]) requires `fastai v0.7`. See [this thread](https://forums.fast.ai/t/fastai-v0-7-install-issues-thread/24652).
