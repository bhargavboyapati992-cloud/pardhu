@echo off
echo ============================================================
echo   Installing Google Cloud SDK (This takes a few minutes...)
echo ============================================================
winget install Google.CloudSDK -e --accept-package-agreements --accept-source-agreements

echo.
echo ============================================================
echo   Google Cloud CLI Installed!
echo   Next Step: Authenticating to your Google Account...
echo   (A browser window will open shortly. Please log in.)
echo ============================================================
REM We have to explicitly call the .cmd from its install location if PATH has not refreshed yet
call "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" auth login

echo.
echo ============================================================
echo   Ready to Deploy to Cloud Run!
echo   (Press any key to build your Docker image and push to Cloud Run)
echo ============================================================
pause

call "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" run deploy smart-plant-watering --source . --port 8080 --allow-unauthenticated

echo Deployment Complete! You can find your public URL above.
pause
