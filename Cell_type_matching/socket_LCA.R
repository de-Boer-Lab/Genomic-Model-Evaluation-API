library(BiocStyle)
library(ontoProc)
library(ontologyPlot)
# for package references
library(igraph)

while(TRUE){
  args = commandArgs(trailingOnly=TRUE)
  print(args)
  writeLines("Listening...")
  con <- socketConnection(host='0.0.0.0', port = 6051, blocking=TRUE,
                          server=TRUE, open="r+")
  data <- readLines(con, 1)
  #data = "{\"evalutor_cell_types\": [\"HepG2\"], \"predictor_cell_types\": [\"iPSC cell line\", \"liver cell line\", \"liver\", \"kidney cell line\", \"hepatoma cell line\", \"hepatoma cell\"]}"
  #print(data)

  #print(jsonlite::fromJSON(txt = data))
  cell_types = jsonlite::fromJSON(txt = data)
  #cell_types$evalutor_cell_types
  #cell_types$predictor_cell_types

  #get the ontology that you need can also load in from a .obo file
  #here we will use a cell line ontology
  clonto = getOnto("cellLineOnto", "2022")

  #extract ontology ids for your evaluator cell type
  #evaluator_cell_ontoids = liberalMap(c("HepG2", "Hep G2", "HEPG2", "HEP-G2","HEP G2", "HEP G2/2.2.1"),clonto)$ontoid
  evaluator_cell_ontoids = liberalMap(cell_types$evalutor_cell_types,clonto)$ontoid

  #extract the ontology ids for the predictor
  #predictor_cell_types = c("iPSC cell line", "liver cell line", "liver", "kidney cell line", "hepatoma cell line", "hepatoma cell")
  predictor_cell_ontoids = liberalMap(cell_types$predictor_cell_types,clonto)$ontoid
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
  #ontoProc:::findCommonAncestors(c("CLO:0003705", "CLO:0000019", "CLO:0000235", "CLO:0002412", "CLO:0037329"), g=onto_graph)

  #it makes the most sense to input only one ontoid for the predictor otherwise the LCA will get messed up
  #here is an example
  #ontoProc:::findCommonAncestors(c("CLO:0003705","CLO:0037359", "CLO:0000019", "CLO:0000235", "CLO:0002412", "CLO:0037329"), g=onto_graph)

  results = ontoProc:::findCommonAncestors(all_ontoids_CL, g=onto_graph)

  #results[1,2]
  #label_TAG(row.names(results)[1], clonto)
  writeLines(label_TAG(row.names(results)[1], clonto), con)
  #writeLines("HEPg2", con)
  close(con)
}
