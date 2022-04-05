
def load_wiki_labels(from_scratch=False) -> SparseLabels:
    # load pickled to avoid generating every time.
    if not from_scratch and SPARSE_LABEL_PATH.is_file():
        with open(SPARSE_LABEL_PATH, "rb") as f:
            return pickle.load(f)
    else:
        log.warning("Node list file not found. Generating...")

        if not DATABASE_PATH.is_file():
            raise IOError('Specified SQLite file "{0}" does not exist.'.format(DATABASE_PATH))

        sdow_conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        labels_df = pd.read_sql("SELECT id, title FROM pages where is_redirect=0", sdow_conn)
        labels_df = labels_df.rename(columns={"id": "article_id"})
        labels_df = labels_df.sort_values(by=["article_id"])
        labels = SparseLabels(labels_df)

        with open(SPARSE_LABEL_PATH, "wb") as f:
            pickle.dump(labels, f)
        return labels


def load_wiki_graph() -> SparseGraph:
    labels: SparseLabels = load_wiki_labels()
    with open(SPARSE_MATRIX_PATH, "rb") as f:
        matrix: sparse.csr_matrix = sparse.load_npz(f)
    graph = SparseGraph(matrix, labels)
    return graph
