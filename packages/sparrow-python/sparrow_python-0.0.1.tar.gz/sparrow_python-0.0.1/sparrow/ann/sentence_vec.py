from rich import print
from sentence_transformers import models, SentenceTransformer

# model_name = 'imxly/sentence_roberta_wwm_ext'  # 'imxly/sentence_rtb3'  #
# word_embedding_model = models.Transformer(model_name)
# pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
#                                pooling_mode_mean_tokens=True,
#                                pooling_mode_cls_token=False,
#                                pooling_mode_max_tokens=False)
# model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
# model = SentenceTransformer('imxly/sentence_roberta_wwm_ext')

# 另一个
# model = SentenceTransformer('cyclone/simcse-chinese-roberta-wwm-ext')
# model = SentenceTransformer('WangZeJun/simbert-base-chinese')
# model = SentenceTransformer('WangZeJun/roformer-sim-base-chinese')
# model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

model = SentenceTransformer('peterchou/simbert-chinese-base')

def evaluate(model, s1, s2):
    """
    余弦相似度计算
    """
    import numpy as np
    v1 = model.encode(s1)
    v2 = model.encode(s2)
    # print(v1.shape)
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    score = v1.dot(v2)
    print(score)
    return score


evaluate(model, '我喜欢那个女生', '我喜欢这个男生')
evaluate(model, 'hello', '你好')
evaluate(model, '上海', '魔都')
evaluate(model, '北京', '帝都')
evaluate(model, '安徽', '皖')
evaluate(model, '我喜欢他', '我不喜欢她')
evaluate(model, '北京', '深圳')


# s1_list = ['北京', '北京', '上海', '上海', '安徽']
# s2_list = ['帝都', '魔都', '帝都', '魔都', '皖']
# evaluate(model, s1_list, s2_list)
