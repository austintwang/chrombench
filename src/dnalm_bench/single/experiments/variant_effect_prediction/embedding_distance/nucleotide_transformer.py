from ..variant_tasks import load_embeddings_and_compute_cosine_distance, load_embeddings_and_compute_l1_distance
from ....embeddings import NucleotideTransformerVariantEmbeddingExtractor
from ....components import VariantDataset
import os
import polars as pl

if __name__ == "__main__":
    model_name = "nucleotide-transformer-v2-500m-multi-species"
    # genome_fa = "/mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta"
    # genome_fa = "/scratch/groups/akundaje/dnalm_benchmark/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta"
    # genome_fa = "/oak/stanford/groups/akundaje/refs/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta"
    genome_fa = "/oak/stanford/groups/akundaje/soumyak/refs/hg19/male.hg19.fa"
    variants_bed = "/oak/stanford/groups/akundaje/anusri/variant-benchmakring/Afr.CaQTLS.tsv"
    batch_size = 2048
    num_workers = 4
    seed = 0
    device = "cuda"
    chroms=None

    h5_file = "nt-500m.Afr.CaQTLS.variant_embeddings.h5"
    # out_dir = "/oak/stanford/groups/akundaje/projects/dnalm_benchmark/embeddings/variant_embeddings/Nucleotide-Transformer/"
    out_dir = "/scratch/groups/akundaje/dnalm_benchmark/embeddings/variant_embeddings/Nucleotide-Transformer/"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, h5_file)

    dataset = VariantDataset(genome_fa, variants_bed, chroms, seed)
    extractor = NucleotideTransformerVariantEmbeddingExtractor(model_name, batch_size, num_workers, device)
    extractor.extract_embeddings(dataset, out_path, progress_bar=True)

    # cosine_distances  = load_embeddings_and_compute_cosine_distance(out_dir, h5_file, progress_bar=True)
    l1_distances = load_embeddings_and_compute_l1_distance(out_dir, h5_file, progress_bar=True)
    print("Number of SNPs =", dataset.__len__())
    # print("Number of Cosine Distances = ", len(cosine_distances))

    df = dataset.elements_df
    # cos_dist = pl.Series('cosine_distances', cosine_distances)
    l1_dist = pl.Series('l1_distances', l1_distances)
    # df = df.with_columns(cos_dist)
    df = df.with_columns(l1_dist)
    # df.write_csv(os.path.join(out_dir, "gena-lm.gm12878.dsqtls.benchmarking.cosine_distances.tsv"), separator="\t")
    df.write_csv(os.path.join(out_dir, "nt.Afr.CaQTLS.l1_distances.tsv"), separator="\t")

