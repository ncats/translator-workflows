#library(pheatmap)
library(RColorBrewer)
#library(e1071)
library(gplots)
library(amap)


hamming.distance <- function(x,y){
  sum(x != y) / length(x)
}


setwd("~/Documents/VIMSS/ontology/NCATS/notebooks/cq-notebooks/Orange_GO_annotation_compendium/")

data <- read.csv("human_disease_phenotype_matrix.txt",sep="\t",row.names=1,header=T)

range <- range(data.matrix(data))
range
dim(data)

class(data.matrix(data))
class(as.matrix(data))

colsums <- colSums(data.matrix(data))
rowsums <- rowSums(data.matrix(data))

#which(colsums > 1)

remrows <- which(rowsums == 0)
remrows1 <- which(rowsums == 1)

remcols <- which(colsums == 0)
remcols1 <- which(colsums == 1)
remcols2 <- which(colsums == 2)
data_great1<- data.matrix(data)[-remrows, ]

dim(data_rowgreat1)

mypalette <- rev(brewer.pal(6, "Blues"))
mypalette <- c(mypalette, brewer.pal(6, "YlOrBr"))

clusterall <- heatmap(data.matrix(data), distfun = function(x) dist(x, method="binary"), scale="none")
save(clusterall, file="human_GO_annotation_matrix_great1_clusterall.Rdata")



load("human_GO_annotation_matrix_great1_clusterall.Rdata")

pdf("human_GO_annotation_matrix_great1_hcl.pdf", height = 20, width = 11)
eval(clusterall$call)
dev.off(2)

png("human_GO_annotation_matrix_great1_hcl.png", height = 1000, width = 800)
eval(clusterall$call)
dev.off(2)



###separate clustering from visualizations

###distance calculation
#col_hamming <- outer(data.matrix(data), data.matrix(data), hamming.distance)
#row_hamming <- outer(t(data.matrix(data)), t(data.matrix(data)), hamming.distance)

###uses amap hcluster
hr <- hcluster(t(data.matrix(data)), method="binary", link="complete",nbproc=4)
save(hr, file="hr.Rdata")
hc <- hcluster(data.matrix(data), method="binary", link="complete",nbproc=4)
save(hc, file="hc.Rdata")

#hr <- hclust(as.dist(1-cor(t(y), method="pearson")), method="complete")
#hc <- hclust(as.dist(1-cor(y, method="spearman")), method="complete")

#cluster_heatmap <- heatmap.2(data.matrix(data), Rowv=as.dendrogram(hr), Colv=as.dendrogram(hc),
#          scale="none", density.info="density", trace="none")

cluster_heatmap <- heatmap(data.matrix(data), Rowv=hr, Colv=hc,
                             scale="none", density.info="density", trace="none")

pdf("human_GO_annotation_matrix_great1_hcl.pdf", height = 11, width = 8.5)
eval(cluster$call)
#heatmap(data.matrix(data), Rowv=as.dendrogram(hr), Colv=as.dendrogram(hc),
#          scale="none", density.info="density", trace="none")

#heatmap(cluster_part)
dev.off(2)




clusterall2 <- heatmap.2(data.matrix(data), distfun = function(x) dist(x, method="binary"),  Rowv=hr, Colv=hc, scale="none", col=mypalette)
save(clusterall2, file="human_GO_annotation_matrix_great1_clusterall2.Rdata")

png("human_GO_annotation_matrix_great1_hcl.png", height = 1200, width = 1000)
eval(clusterall2$call)
#heatmap(data.matrix(data), Rowv=as.dendrogram(hr), Colv=as.dendrogram(hc),
#          scale="none", density.info="density", trace="none")

#heatmap(cluster_part)
dev.off(2)


clusterall2 <- heatmap.2(data.matrix(data), distfun = function(x) dist(x, method="binary"),  Rowv=hr, Colv=hc, scale="none", col=mypalette)
save(clusterall2, file="human_GO_annotation_matrix_great1_clusterall2.Rdata")


save(hr, file="cluster_hr.Rdata")
save(hc, file="cluster_hc.Rdata")
save(cluster_heatmap, file="cluster_heatmap.Rdata")

reordered_data <- data.matrix(data)[rev(hr$labels[hr$order]), hc$labels[hc$order]]
write.table(reordered_data, file="human_GO_annotation_matrix_great1_2DHCLorder.txt")



#heatmap(data.matrix(data), distfun = function(x) as.dist(hamming.distance(x)))
#heatmap.2(as.matrix(data2) , trace="none", col=mypalette)#, distfun=function(x) as.dist((1-cor(t(x)))/2))
#pheatmap(t(mat),dist=cordata,breaks=breaks,color=mypalette,show_rownames=F,show_colnames=F,legend=F)

###testing

data100 <- read.csv("human_GO_annotation_matrix_great1_part100.txt",sep="\t",row.names=1,header=T)
row.names(data100) <- data100[,1]
data100 <- data100[,-1]
head(data100)
heatmap(data.matrix(data100), distfun = function(x) dist(x, method="binary"))
