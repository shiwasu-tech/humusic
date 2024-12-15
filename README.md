# jsonにおけるパスの指定方法

生成用スクリプトがあるディレクトリ内に以下の形式でpathを保存したjsonを作成する必要があります．

```json
{   
    "Darwin": {
        "dataset_name": {
            "dataset_dir" : "full path to dataset directry(EX: /datasets/xx, NOT /datasets)",
            "tokenizer_path" : "full path to save tokenizer",
            "chunks_dir" : "full path to save formatted dataset"
        }
    },
    "Windows": {
        "dataset1_name": {
            "dataset_dir" : "C:/Users/...",
            "tokenizer_path" : "...",
            "chunks_dir" : "..."
        },
        "dataset2_name": {
            "dataset_dir" : "C:/Users/...",
            "tokenizer_path" : "...",
            "chunks_dir" : "..."
        }
    }
}
```




dataset from "maestro-v3.0.0"

Curtis Hawthorne, Andriy Stasyuk, Adam Roberts, Ian Simon, Cheng-Zhi Anna Huang,
  Sander Dieleman, Erich Elsen, Jesse Engel, and Douglas Eck. "Enabling
  Factorized Piano Music Modeling and Generation with the MAESTRO Dataset."
  In International Conference on Learning Representations, 2019.