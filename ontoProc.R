library(ontoProc)
library(ontologyPlot)
library(BiocStyle)  # for package references
cl = getOnto("cellOnto", "2022")
go = getOnto("goOnto", "2021")  
pr = getOnto("PROnto", "2021")

data(packDesc2022)
knitr::kable(packDesc2022[,-c(1,7)])

knitr::kable(stab <- seur3kTab())

onto_plot2(cl, stab$tag)

cands = c("astrocyte$", "oligodendrocyte", "oligodendrocyte precursor",
          "neoplastic", "^neuron$", "^vascular", "badterm")
co = ontoProc::getCellOnto()
co = getOnto("cellOnto", year_added="2022")
liberalMap(cands, co)
liberalMap("cancer", co)
liberalMap(cands, co)
onto_plot2(co, PR:P35918)

co <- getOnto("cellOnto")
# TODO: wrap in utility function.
parents <- cl$parents
self <- rep(names(parents), lengths(parents))
library(igraph)
g <- make_graph(rbind(unlist(parents), self))
# Selecting random terms:
LCA <- ontoProc:::findCommonAncestors(A=sample(names(V(g)), 20), B=sample(names(V(g)), 20), g=g)


LCA[1,]
LCA[1,"descendents"][[1]]
clonto = getOnto("cellLineOnto", "2022")
chk = c("CLO:0003702", "CLO:0003703", "CLO:0003704", "CLO:0003705", 
        "CLO:0003706", "CLO:0037329")
onto_plot2(clonto, c("CLO:0003704","CLO:0000235","CLO:0003705","CLO:0037325","CLO:0050716"))
chk = c("CLO:0003704","CLO:0000235")

parents <- clonto$parents
self <- rep(names(parents), lengths(parents))
library(igraph)
g <- make_graph(rbind(unlist(parents), self))

ontoProc:::findCommonAncestors(c("CLO:0003704","CLO:0050716"), g=g)



LCA <- ontoProc:::findCommonAncestors(c("CLO:0003704","CLO:0000235","CLO:0003705", ), g=g)

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

