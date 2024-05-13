import os

from ....embeddings import SequenceBaselineSimpleEmbeddingExtractor
from ....components import SimpleSequence


if __name__ == "__main__":
    model_name = "sequence_baseline"
    genome_fa = "/oak/stanford/groups/akundaje/refs/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta"
    # genome_fa = "/mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta"

    elements_tsv = "/oak/stanford/groups/akundaje/projects/dnalm_benchmark/cell_line_data/peaks_by_cell_label_unique_dataloader_format.tsv"    
    chroms = None
    batch_size = 64
    num_workers = 4
    seed = 0
    device = "cuda"

    out_path = f"/scratch/groups/akundaje/dnalm_benchmark/embeddings/peak_classification_sequence_baseline/{model_name}.h5"

    dataset = SimpleSequence(genome_fa, elements_tsv, chroms, seed)
    extractor = SequenceBaselineSimpleEmbeddingExtractor(batch_size, num_workers, device)
    extractor.extract_embeddings(dataset, out_path, progress_bar=True)