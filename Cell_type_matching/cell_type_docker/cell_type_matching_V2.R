#library(tidyverse)
library(BiocStyle)
library(ontoProc)
#library(ontologyPlot)
  # for package references
library(igraph)


#args <- commandArgs(trailingOnly = TRUE)
#cat(args, sep = "\n")

#get the ontology that you need can also load in from a .obo file
#here we will use a cell line ontology
clonto = getOnto("cellLineOnto", "2022")

#extract ontology ids for your evaluator cell type
evaluator_cell_ontoids = liberalMap(c("HepG2", "Hep G2", "HEPG2", "HEP-G2","HEP G2", "HEP G2/2.2.1"),clonto)$ontoid

#extract the ontology ids for the predictor
predictor_cell_types = c("iPSC cell line", "liver cell line", "liver", "kidney cell line", "hepatoma cell line", "hepatoma cell")
predictor_cell_ontoids = liberalMap(predictor_cell_types,clonto)$ontoid
#stack together to get a ontology plot of the evaluator and predictor cells
all_ontoids = c(evaluator_cell_ontoids, predictor_cell_ontoids)

all_ontoids_CL <- all_ontoids[grep("CLO", (all_ontoids))]

onto_plot2(clonto, all_ontoids)
onto_plot2(clonto,all_ontoids_CL)
#get all the parents from the ontology and create graph
parents <- clonto$parents
print(parents)
self <- rep(names(parents), lengths(parents))
onto_graph <- make_graph(rbind(unlist(parents), self))

#an example that works
#if you take the LCA with the least amount of ancestors or the first row from the data frame
ontoProc:::findCommonAncestors(c("CLO:0003705", "CLO:0000019", "CLO:0000235", "CLO:0002412", "CLO:0037329"), g=onto_graph)

#it makes the most sense to input only one ontoid for the predictor otherwise the LCA will get messed up
#here is an example
ontoProc:::findCommonAncestors(c("CLO:0003705","CLO:0037359", "CLO:0000019", "CLO:0000235", "CLO:0002412", "CLO:0037329"), g=onto_graph)

ontoProc:::findCommonAncestors(all_ontoids_CL, g=onto_graph)



onto_plot2(clonto, evaluator_cell_ontoids)

parents <- clonto$parents
self <- rep(names(parents), lengths(parents))
library(igraph)
g <- make_graph(rbind(unlist(parents), self))

ontoProc:::findCommonAncestors(c("CLO:0003704"),c("CLO:0050716", "CLO:0037325"), g=g)



LCA <- ontoProc:::findCommonAncestors(c("CLO:0003704","CLO:0000235","CLO:0003705" ), g=g)

cands = c("astrocyte$", "oligodendrocyte", "oligodendrocyte precursor",
          "neoplastic", "^neuron$", "^vascular", "badterm")

liberalMap(cands, clonto)

liberalMap("HEP",clonto)
liberalMap("Hep",clonto)


parents <- bto$parents
self <- rep(names(parents), lengths(parents))
library(igraph)
g <- make_graph(rbind(unlist(parents), self))
tmp = liberalMap("HEP",bto)
test = liberalMap("Hep",bto)
liver = liberalMap(c("iPSC", 'HEP', 'liver'), bto)
onto_plot2(bto, liver$ontoid)
ontoProc:::findCommonAncestors(c("BTO:0003477", "BTO:0002895"), g=g)

tmp = liberalMap("Hep-G2",bto)

# #load whatever ontology you want
# #here we will use the Brenda tissue ontology 
# library(igraph)
# library(ontoProc)
# library(ontologyPlot)
# 
# bto = get_ontology("/Users/ishika/Desktop/API/Cell_ontology/bto.obo")
# 
# parents_bto <- bto$parents
# self <- rep(names(parents_bto), lengths(parents_bto))
# 
# onto_graph <- make_graph(rbind(unlist(parents_bto), self))
# evaluator_cell_types = "HepG2"
# predictor_cell_types = c("iPSC cell line", "liver cell line", "liver", "kidney cell line", "hepatoma cell line", "hepatoma cell")
# 
# #lca_cellType <- function(predictor_cell_types, evaluator_cell_types){
# 
# #first use liberal map to find cell types/cell lines in the ontology that are similar
# evaluator_cell_ontoids = liberalMap("Hep-G2",bto)$ontoid
# 
# predictor_cell_ontoids = liberalMap(predictor_cell_types,bto)$ontoid
# all_ontoids = c(evaluator_cell_ontoids, predictor_cell_ontoids)
# onto_plot2(bto, all_ontoids)
# ontoProc:::findCommonAncestors(c(evaluator_cell_ontoids, predictor_cell_ontoids), g=onto_graph)
# 
# 
# lca_match = "HEPG2"
# result <- paste0("The predictor will use: ",lca_match," as the cloest matched cell type")
# return(result)
# 
# 
# lca_cellType(1,2)
# 
# 
# 
# parents_bto <- cl$parents
# self <- rep(names(parents_bto), lengths(parents_bto))
# 
# onto_graph <- make_graph(rbind(unlist(parents_bto), self))
# evaluator_cell_types = "HepG2"
# predictor_cell_types = c("iPSC cell line", "liver cell line", "liver", "kidney cell line", "hepatoma cell line", "hepatoma cell")
# 
# #lca_cellType <- function(predictor_cell_types, evaluator_cell_types){
# 
# #first use liberal map to find cell types/cell lines in the ontology that are similar
# evaluator_cell_ontoids = liberalMap("Hep-G2",cl)$ontoid
# 
# predictor_cell_ontoids = liberalMap(predictor_cell_types,cl)$ontoid
# all_ontoids = c(evaluator_cell_ontoids, predictor_cell_ontoids)
# onto_plot2(cl, all_ontoids)
# ontoProc:::findCommonAncestors(c(evaluator_cell_ontoids, predictor_cell_ontoids), g=onto_graph)
# 
# 
# lca_match = "HEPG2"
# result <- paste0("The predictor will use: ",lca_match," as the cloest matched cell type")
# return(result)
# 
# cl = ontoProc::getOnto('cellOnto')
# cl3k = c("CL:0000492", "CL:0001054", "CL:0000236", "CL:0000625",
#          "CL:0000576", "CL:0000623", "CL:0000451", "CL:0000556","CL:0000988")
# ontoProc::onto_plot2(cl, cl3k)
# 
# 
# parents <- cl$parents
# self <- rep(names(parents), lengths(parents))
# library(igraph)
# g <- make_graph(rbind(unlist(parents), self))
# ontoProc:::findCommonAncestors(c("CL:0000988"), c("CL:0000842", "CL:0000576", "CARO:0000006", "CL:0000556"), g=g)
# 
