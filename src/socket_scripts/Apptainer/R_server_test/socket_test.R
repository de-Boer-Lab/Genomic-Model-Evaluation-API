server <- function(){
  while(TRUE){
    writeLines("Listening...")
    con <- socketConnection(host="172.16.47.244", port = 8021, blocking=TRUE,
                            server=TRUE, open="r+")
    data <- readLines(con, 1)
    print(data)
    response <- toupper(data)
    writeLines(response, con)
    close(con)
  }
}
server()
