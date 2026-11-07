@echo off
set "CATALINA_HOME=C:\Program Files\Apache Software Foundation\Tomcat 9.0_Tomcat99"
set "CATALINA_BASE=C:\Users\chait\eclipse-web-workspace\.metadata\.plugins\org.eclipse.wst.server.core\tmp0"
set "WTP_DEPLOY=%CATALINA_BASE%\wtpwebapps"

java -Dcatalina.base="%CATALINA_BASE%" -Dcatalina.home="%CATALINA_HOME%" -Dwtp.deploy="%WTP_DEPLOY%" -Djava.library.path="%CATALINA_HOME%\bin" --enable-native-access=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED -cp "%CATALINA_HOME%\bin\bootstrap.jar;%CATALINA_HOME%\bin\tomcat-juli.jar" org.apache.catalina.startup.Bootstrap start
