Tests <- read.csv("D:\\Wali\\amrbd_datbasein_csv\\STATICBAHIS_sglisampletests_202207251225.csv", header=TRUE, stringsAsFactors=TRUE)
Samples <- read.csv("D:\\Wali\\amrbd_datbasein_csv\\STATICBAHIS_sglisamples_202207251225.csv", header=TRUE, stringsAsFactors=TRUE)
Antibiotics <- read.csv("D:\\Wali\\amrbd_datbasein_csv\\STATICBAHIS_antibiotics_202207251225.csv", header=TRUE, stringsAsFactors=TRUE)
Pathogens <- read.csv("D:\\Wali\\amrbd_datbasein_csv\\STATICBAHIS_pathogen_202207251225.csv", header=TRUE, stringsAsFactors=TRUE)
Species <- read.csv("D:\\Wali\\amrbd_datbasein_csv\\STATICBAHIS_species_202207251225.csv", header=TRUE, stringsAsFactors=TRUE)
Specimen <- read.csv("D:\\Wali\\amrbd_datbasein_csv\\STATICBAHIS_specimens_202207251225.csv", header=TRUE, stringsAsFactors=TRUE)
SpecimenCat <- read.csv("D:\\Wali\\amrbd_datbasein_csv\\STATICBAHIS_specimen_categories_202207251225.csv", header=TRUE, stringsAsFactors=TRUE)
Sensitivity <- read.csv("D:\\Wali\\amrbd_datbasein_csv\\STATICBAHIS_testsensitivities_202207251225.csv", header=TRUE, stringsAsFactors=TRUE)
TestMethods <- read.csv("D:\\Wali\\amrbd_datbasein_csv\\STATICBAHIS_testmethods_202207251225.csv", header=TRUE, stringsAsFactors=TRUE)

nrow(Samples[Samples$specimen_id == 28, ])

#Cleaning up the tables by getting rid of unneeded columns
TestsCleaned = subset(Tests, select = -c(pathogen_id, created_by, created_at, 
                                                  updated_at))
SamplesCleaned = subset(Samples, select = -c(created_by, created_at, 
                                         updated_at))
AntibioticsCleaned = subset(Antibiotics, select = -c(created_by, created_at, 
                                             updated_at))
PathogensCleaned = subset(Pathogens, select = -c(created_by, created_at, 
                                             updated_at))
SpecimenCleaned = subset(Specimen, select = -c(created_by, created_at, 
                                             updated_at))
SensitivityCleaned = subset(Sensitivity, select = -c(created_by, created_at, 
                                               updated_at))
TestMethodsCleaned = subset(TestMethods, select = -c(created_by, created_at, 
                                               updated_at))

#Merging the tables, so that we have one table containing all the data
TestsUpdated <- merge(x=TestsCleaned, y=SamplesCleaned, by="sample_id", all.x=TRUE)
TestsUpdated_1 <- merge(x=TestsUpdated, y=AntibioticsCleaned, by="antibiotic_id", all.x=TRUE)
TestsUpdated_2 <- merge(x=TestsUpdated_1, y=PathogensCleaned, by="pathogen_id", all.x=TRUE)
TestsUpdated_3 <- merge(x=TestsUpdated_2, y=SpecimenCleaned, by="specimen_id", all.x=TRUE)
TestsUpdated_4 <- merge(x=TestsUpdated_3, y=SpecimenCat, by="specimen_category_id", all.x=TRUE)
TestsUpdated_5 <- merge(x=TestsUpdated_4, y=TestMethodsCleaned, by="test_method_id", all.x=TRUE)
InputTable <- merge(x=TestsUpdated_5, y=SensitivityCleaned, by="test_sensitivity_id", all.x=TRUE)

nrow(InputTable[InputTableCleaned$specimen_category_name == "Urinary", ])

#Cleaning the InputTable by removing unneeded columns
InputTableCleaned = subset(InputTable, select = -c(test_id, antibiotic_id, pathogen_id, test_method_id,
                                                   specimen_id, specimen_category_id, test_sensitivity_id,
                                                   specimen_alt_names, pathogen_alt_names, antibiotic_alt_names))

#Let's try extracting from InputTable Cleaned before calc (extra stuff)

InputTableUrine <- subset(InputTableCleaned, InputTableCleaned$specimen_category_name == 'Urinary')


sum(FinalOutputTable.Urinary$TotalCount)


SampleUp <- merge(x=SamplesCleaned, y=SpecimenCleaned, by="specimen_id", all.x=TRUE)
SampleUp_2 <- merge(x=SampleUp, y=SpecimenCat, by="specimen_category_id", all.x=TRUE)

write.xlsx(SampleUp_2, file = "D:\\Wali\\amrbd_datbasein_csv\\Sample Table.xlsx")

#Come here after clearing the sorting problem
#Generating an output table
OutputTable = data.frame(Antibiotic = c(InputTableCleaned$antibiotic_name),
  Pathogen = c(InputTableCleaned$pathogen_name),
  Specimen = c(InputTableCleaned$specimen_category_name),
  Sensitivity = c(InputTableCleaned$test_sensitivity_type),
  stringsAsFactors = TRUE

)



OutputTable <- data.frame(
OutputTable1 <- InputTableCleaned %>%
  group_by(specimen_category_name, antibiotic_name, pathogen_name) %>%
  summarise(Count_S = n_distinct(Sensitivity == 'S')),
  
OutputTable2 <- InputTableCleaned %>%
  group_by(specimen_category_name, antibiotic_name, pathogen_name) %>%
  summarise(Count_I = n_distinct(Sensitivity == 'I')),

OutputTable3 <- InputTableCleaned %>%
  group_by(specimen_category_name, antibiotic_name, pathogen_name) %>%
  summarise(Count_R = n_distinct(Sensitivity == 'R'))

)

#Cleaning the output table

FinalOutputTable = subset(OutputTable, select = -c(specimen_category_name.1, antibiotic_name.1, pathogen_name.1,
                                                   specimen_category_name.2, antibiotic_name.2, pathogen_name.2))

View(FinalOutputTable)

#Calculating Total count and adding them to a new column
FinalOutputTable$TotalCount = rowSums(FinalOutputTable[,c("Count_S", "Count_I", "Count_R")])
# Calculating sensitivity as percentage of total count
FinalOutputTable$SensistivityPercent <- FinalOutputTable$Count_S/FinalOutputTable$TotalCount 

#Exporting the Table as an excel file

#Step 1. Separating the Final Output Table into smaller tables according to "Specimen"
for(i in unique(FinalOutputTable$Specimen)) {
  nam <- paste('FinalOutputTable', i, sep = ".")
  assign(nam, FinalOutputTable[FinalOutputTable$Specimen==i,])
  
}

#Step 2. Creating a workbook with multiple tables

SpecimenWiseTable <- list("Abcess" = `FinalOutputTable.Abscess`,
                          "Blood" = FinalOutputTable.Blood,
                          "Bone" = `FinalOutputTable.Bone`,
                          "ENT" = `FinalOutputTable.ENT`,
                          "Eye" = `FinalOutputTable.Eye`,
                          "Lower Respiratory Tract" = `FinalOutputTable.Lower Respiratory`,
                          "Upper Respiratory Tract" = `FinalOutputTable.Upper Respiratory`,
                          "Stomach" = `FinalOutputTable.Stomach`,
                          "Vagina" = `FinalOutputTable.Vaginal`,
                          "Urine" = `FinalOutputTable.Urinary`,
                          "Sputum" = FinalOutputTable.Sputum,
                          "Stool" = FinalOutputTable.Stool,
                          "Wound" = `FinalOutputTable.Wound`
                          
)

#3. Exporting as excel file with multiple sheets
write.xlsx(SpecimenWiseTable, file = "D:\\Wali\\amrbd_datbasein_csv\\Specimen Wise Table.xlsx")

write.xlsx(OutputTable, file = "D:\\Wali\\amrbd_datbasein_csv\\Output Table.xlsx")
write.xlsx(FinalOutputTable, file = "D:\\Wali\\amrbd_datbasein_csv\\Final Output Table.xlsx")
write.xlsx(InputTableCleaned, file = "D:\\Wali\\amrbd_datbasein_csv\\Input Table (clean).xlsx")

