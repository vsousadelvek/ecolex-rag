"""Script para ingestão de legislação ambiental brasileira.

Uso:
    python -m scripts.ingest                          # Ingere todas as leis do diretório data/legislation/
    python -m scripts.ingest --file caminho/lei.txt   # Ingere um arquivo específico
    python -m scripts.ingest --download               # Baixa e ingere as leis principais
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.services.embeddings import embedding_service
from app.services.knowledge_graph import kg_service
from app.services.retriever import bm25_service
from app.services.ingestion import ingest_legislation

# Legislações ambientais brasileiras de referência
SAMPLE_LEGISLATION = {
    "Código Florestal - Lei 12.651/2012": "codigo_florestal.txt",
    "PNMA - Lei 6.938/1981": "pnma.txt",
    "SNUC - Lei 9.985/2000": "snuc.txt",
    "Lei de Crimes Ambientais - Lei 9.605/1998": "crimes_ambientais.txt",
    "Resolução CONAMA 357/2005": "conama_357.txt",
    "Resolução CONAMA 430/2011": "conama_430.txt",
    "Resolução CONAMA 302/2002": "conama_302.txt",
    "Resolução CONAMA 303/2002": "conama_303.txt",
}


def main():
    parser = argparse.ArgumentParser(description="Ingestão de legislação ambiental")
    parser.add_argument("--file", type=str, help="Caminho para arquivo de legislação")
    parser.add_argument("--name", type=str, help="Nome da lei")
    parser.add_argument("--dir", type=str, default=settings.legislation_path, help="Diretório com legislações")
    args = parser.parse_args()

    print("Inicializando serviços...")
    embedding_service.load()
    bm25_service.load()
    kg_service.load()

    if args.file:
        name = args.name or Path(args.file).stem
        print(f"\nIngerindo: {name}")
        result = ingest_legislation(law_name=name, file_path=args.file)
        print(f"  Chunks: {result.chunks_created}")
        print(f"  Triplets: {result.triplets_extracted}")
    else:
        leg_dir = Path(args.dir)
        if not leg_dir.exists():
            print(f"Diretório {leg_dir} não encontrado.")
            print("Crie o diretório e adicione os arquivos .txt ou .pdf das legislações.")
            print(f"\nArquivos esperados:")
            for law_name, filename in SAMPLE_LEGISLATION.items():
                print(f"  {leg_dir / filename}  ->  {law_name}")
            return

        files = list(leg_dir.glob("*.txt")) + list(leg_dir.glob("*.pdf"))
        if not files:
            print(f"Nenhum arquivo .txt ou .pdf encontrado em {leg_dir}")
            return

        # Mapear nomes conhecidos
        name_map = {v: k for k, v in SAMPLE_LEGISLATION.items()}

        for f in sorted(files):
            law_name = name_map.get(f.name, f.stem)
            print(f"\nIngerindo: {law_name}")
            try:
                result = ingest_legislation(law_name=law_name, file_path=str(f))
                print(f"  Chunks: {result.chunks_created}")
                print(f"  Triplets: {result.triplets_extracted}")
            except Exception as e:
                print(f"  ERRO: {e}")

    print("\nIngestão concluída!")
    print(f"Total chunks FAISS: {embedding_service.total_chunks}")
    print(f"Total chunks BM25: {bm25_service.total_chunks}")
    print(f"Total triplets KG: {kg_service.total_triplets}")


if __name__ == "__main__":
    main()
