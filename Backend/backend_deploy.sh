#!/bin/bash

if [ -d "$DEST_DIR/Model-based-software-design" ]; then
	echo "The directory exist."
else
	git clone https://github.com/Darrenchenn/Model-based-software-design.git
fi

# 定义目标目录路径
DEST_DIR="/root"

# 备份原有Backend目录（如果存在）
if [ -d "$DEST_DIR/Backend" ]; then
  rm -r $DEST_DIR/Backend_backup $DEST_DIR/FrontEnd_backup
  mv $DEST_DIR/Backend $DEST_DIR/Backend_backup
fi

# 复制新的Backend目录
rsync -a $DEST_DIR/Model-based-software-design/Backend/ $DEST_DIR/Backend

# 备份原有Frontend目录（如果存在）
if [ -d "$DEST_DIR/FrontEnd" ]; then
  mv $DEST_DIR/FrontEnd $DEST_DIR/FrontEnd_backup
fi

# 复制新的FrontEnd目录
rsync -a $DEST_DIR/Model-based-software-design/FrontEnd/ $DEST_DIR/FrontEnd

# 删除临时目录
rm -r $DEST_DIR/Model-based-software-design/

#!/bin/bash

# 杀掉8000端口的进程
echo "Killing processes running on port 8000..."
kill -9 $(lsof -t -i:8000) 2>/dev/null

# 进入指定目录
cd $DEST_DIR/Backend/

# 启动Django开发服务器
echo "Starting Django development server on 0.0.0.0:8000..."
source $DEST_DIR/newenv/bin/activate
python3 manage.py runserver 0.0.0.0:8000 &

sleep 5
# 输出完成信息
echo "ZIP文件已解压，Backend&FrontEnd目录已替换，临时目录已删除。"
ss -tulp | grep 800
