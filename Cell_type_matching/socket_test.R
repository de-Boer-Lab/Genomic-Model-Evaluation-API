server <- function(){
  while(TRUE){
    writeLines("Listening...")
    con <- socketConnection(host="localhost", port = 6013, blocking=TRUE,
                            server=TRUE, open="r+")
    data <- readLines(con, 1)
    print(data)
    response <- toupper(data) 
    writeLines(response, con) 
    close(con)
  }
}
server()