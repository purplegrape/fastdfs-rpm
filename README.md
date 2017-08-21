# fastdfs-rpm
fastdfs  rpm spec file for CentOS

#prepare
yum install rpm-build gcc gcc-c++ libtool make autoconf -y

#build:

cd ~
git clone https://github.com/purplegrape/fastdfs-rpm
mv fastdfs-rpm rpmbuild
cd rpmbuild/SPEC/
rpmbuild -ba fastdfs.spec

