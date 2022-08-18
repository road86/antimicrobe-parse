library('dplyr')

rm(list = ls())

#Loading csv file
cleaneddata <- read.csv("outdata/ast_data_clean.csv", header=TRUE)

# Creating a grouped data to count R, I and S
OutputTable <- data.frame(
  OutputTable1 <- cleaneddata %>%
    group_by(specimen_category, pathogen, antibiotic) %>%
    summarise(count_s = sum(sensitivity == 's')),

  OutputTable2 <- cleaneddata %>%
    group_by(specimen_category, pathogen, antibiotic) %>%
    summarise(count_i = sum(sensitivity == 'i')),

  OutputTable3 <- cleaneddata %>%
    group_by(specimen_category, pathogen, antibiotic) %>%
    summarise(count_r = sum(sensitivity == 'r'))

)
# Cleaning the output table
FinalOutputTable = subset(OutputTable, select = -c(antibiotic.1, pathogen.1, specimen_category.1,
                                                   antibiotic.2, pathogen.2, specimen_category.2))

#Calculating Total count and adding them to a new column
FinalOutputTable$total = rowSums(FinalOutputTable[,c("count_s", "count_i", "count_r")])
# Calculating sensitivity as percentage of total count
FinalOutputTable$sensitivity <- FinalOutputTable$count_s/FinalOutputTable$total

write.csv(FinalOutputTable,'pre-processed.csv')

isolates <- cleaneddata %>%
  group_by(specimen_category, pathogen)%>%
  summarise(n_distinct(amr_uuid))
colnames(isolates) <- c('specimen_category','pathogen','number_of_isolates')
write.csv(isolates,'number_of_isolates.csv')
