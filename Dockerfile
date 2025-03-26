FROM mcr.microsoft.com/windows/servercore:ltsc2019

WORKDIR /app

COPY SPIDYNAL.exe .
COPY run_spidynal.bat .

CMD ["cmd.exe", "/c", "run_spidynal.bat"]
