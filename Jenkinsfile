node('centos7-mono4') {
  stage 'Build and Deploy'
  env.PATH = "${tool 'apache-maven-3.0.5'}/bin:${env.PATH}"
  checkout scm
  sh 'mvn clean deploy'
}
