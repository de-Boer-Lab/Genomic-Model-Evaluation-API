library(ontoProc)
library(ontologyPlot)
library(BiocStyle)  # for package references
library(igraph)

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
self <- rep(names(parents), lengths(parents))
onto_graph <- make_graph(rbind(unlist(parents), self))

#an example that works
#if you take the LCA with the least amount of ancestors or the first row from the data frame

LCA <- ontoProc:::findCommonAncestors(A = c("CLO:0003705"), B=c("CLO:0000019", "CLO:0000235", "CLO:0002412","CLO:0037329"), g=onto_graph, remove.self = TRUE)
ontoProc:::findCommonAncestors(c("CLO:0003705","CLO:0000019", "CLO:0000235", "CLO:0002412","CLO:0037329"), g=onto_graph)

LCA <- ontoProc:::findCommonAncestors(A = c("CLO:0003705"), B=c("CLO:0037329", "CLO:0000019", "CLO:0000235", "CLO:0037360"), g=onto_graph, remove.self = TRUE)
ontoProc:::findCommonAncestors(A = c("CLO:0003705"), B=c("CLO:0037360"), g=onto_graph, remove.self = TRUE)
ontoProc:::findCommonAncestors(A = c("CLO:0000042"), B=c("CLO:0037329","CLO:0000235"), g=onto_graph, remove.self = TRUE)

#it makes the most sense to input only one ontoid for the predictor otherwise the LCA will get messed up
#here is an example
ontoProc:::findCommonAncestors(c("CLO:0003705","CLO:0037359", "CLO:0000019", "CLO:0000235", "CLO:0002412", "CLO:0037329"), g=onto_graph)

ontoProc:::findCommonAncestors(all_ontoids_CL, g=onto_graph)


evaluator_cell_types = c("HepG2", "Hep G2", "HEPG2", "HEP-G2","HEP G2", "HEP G2/2.2.1")
predictor_cell_types = c("iPSC cell line", "liver cell line", "liver", "kidney cell line", "hepatoma cell line", "hepatoma cell")

lca_cellType <- function(clonto, predictor_cell_types, evaluator_cell_types){
  evaluator_cell_ontoids = liberalMap(evaluator_cell_types,clonto)$ontoid
  
  #extract the ontology ids for the predictor
  predictor_cell_types = predictor_cell_types
  predictor_cell_ontoids = liberalMap(predictor_cell_types,clonto)$ontoid
  #stack together to get a ontology plot of the evaluator and predictor cells
  all_ontoids = c(evaluator_cell_ontoids, predictor_cell_ontoids)
  
  all_ontoids_CL <- all_ontoids[grep("CLO", (all_ontoids))]
  
  onto_plot2(clonto, all_ontoids)
  onto_plot2(clonto,all_ontoids_CL)
  #get all the parents from the ontology and create graph
  parents <- clonto$parents
  self <- rep(names(parents), lengths(parents))
  onto_graph <- make_graph(rbind(unlist(parents), self))
  
  #an example that works
  #if you take the LCA with the least amount of ancestors or the first row from the data frame
  lca = ontoProc:::findCommonAncestors(c("CLO:0003705", "CLO:0000019", "CLO:0000235", "CLO:0002412", "CLO:0037329"), g=onto_graph)
  lca_match = lca[1,]
  #print(clonto$name[row.names(lca_match)])
  result <- paste0("The predictor will use: ",clonto$name[row.names(lca_match)]," as the closest matched cell type")
  return(result)
  
}
lca_cellType(clonto, predictor_cell_types, evaluator_cell_types)


