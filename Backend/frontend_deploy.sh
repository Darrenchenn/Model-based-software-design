#!/bin/bash
DEST_DIR="/root"


# Step 2: 进入目录
cd $DEST_DIR/Model-based-software-design/FrontEnd/an-intelligent-image-and-text-creation-system
if [ $? -ne 0 ]; then
    echo "进入目录失败"
    exit 1
fi

npm install 
if [ $? -ne 0 ]; then
    echo "npm run install 失败"
    exit 1
fi
# Step 3: 执行npm run build
npm run build
if [ $? -ne 0 ]; then
    echo "npm run build 失败"
    exit 1
fi

# Step 4: 删除旧的dist目录
rm -rf /usr/share/nginx/html/dist
if [ $? -ne 0 ]; then
    echo "删除旧的dist目录失败"
    exit 1
fi

# Step 5: 拷贝新生成的dist目录
cp -r dist /usr/share/nginx/html/
if [ $? -ne 0 ]; then
    echo "拷贝新的dist目录失败"
    exit 1
fi


# Step 6: 删除解压后的文件夹
rm -rf $DEST_DIR/Model-based-software-design-feature-1.1

echo "脚本执行成功"

systemctl restart nginx
systemctl status nginx
