FROM mcr.microsoft.com/windows/servercore:ltsc2019

WORKDIR /app

# Copy the entire repo structure, including SPIDYNAL.exe and \build\spidy\mound\
COPY . .

# Set the entrypoint to run SPIDYNAL.exe with the provided command
ENTRYPOINT ["SPIDYNAL.exe"]
