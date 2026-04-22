# Collapse_GTDB_Phylotree
Collapse GTDB bacterial phylogenetic tree using ETE3 package

This script processes a GTDB phylogenetic tree and collapses it to the genus level using the ETE3 toolkit.
This project depends on ETE3 (GPLv3). Please install it separately.

It removes species-level nodes, normalizes node labels, and outputs a cleaned Newick tree that preserves higher taxonomic hierarchy (family, order, class, phylum, domain).


## 🔧 Features
- Removes bootstrap prefixes (e.g., `100:g__X → g__X`)
- Collapses tree to **genus level**
- Removes species nodes (`s__`)
- Preserves higher taxonomy:
  - family (`f__`)
  - order (`o__`)
  - class (`c__`)
  - phylum (`p__`)
  - domain (`d__`)
- Automatically fixes:
  - empty labels → replaced with `UNLABELED_x`
  - labels containing spaces → quoted (`'...'`)
- Outputs a clean and parser-compatible Newick tree

## 📂 Input
- GTDB tree file
  Example: bac120.sp_labels.tree

## 📤 Output
- Collapsed tree at genus level

## 🧪 Requirements
- Python 3.6+
- ETE3
