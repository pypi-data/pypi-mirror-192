from milvus_utils import get_milvus_collection, efficientnet_b7
from sparrow import relp, ls
from towhee.types.image_utils import from_pil
import towhee

path_list = ls('./milvus_db/data/ring/', '*.jpg')
collection, id_path_dict = get_milvus_collection(
    path_list,
    "image_search",
    rebuild=False
)

search_function = (
    towhee.dummy_input()
    .runas_op(func=lambda img: from_pil(img))
    .runas_op['img', 'vec'](func=efficientnet_b7)
    .tensor_normalize()
    .ann_search.milvus(uri=milvus_uri, limit=5)
    .runas_op(func=lambda res: [x.id for x in res])
    .as_function()
)
