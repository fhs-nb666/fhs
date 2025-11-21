# fhs

## 如何关联远程仓库 (How to Associate a Remote Repository)

### 中文说明

#### 1. 添加远程仓库
```bash
git remote add origin <远程仓库URL>
```
例如：
```bash
git remote add origin https://github.com/username/repository.git
```

#### 2. 查看远程仓库
```bash
git remote -v
```

#### 3. 修改远程仓库URL
```bash
git remote set-url origin <新的远程仓库URL>
```

#### 4. 删除远程仓库
```bash
git remote remove origin
```

#### 5. 推送代码到远程仓库
```bash
git push -u origin main
```

#### 6. 从远程仓库拉取代码
```bash
git pull origin main
```

### English Instructions

#### 1. Add a Remote Repository
```bash
git remote add origin <remote-repository-URL>
```
Example:
```bash
git remote add origin https://github.com/username/repository.git
```

#### 2. View Remote Repositories
```bash
git remote -v
```

#### 3. Change Remote Repository URL
```bash
git remote set-url origin <new-remote-repository-URL>
```

#### 4. Remove a Remote Repository
```bash
git remote remove origin
```

#### 5. Push Code to Remote Repository
```bash
git push -u origin main
```

#### 6. Pull Code from Remote Repository
```bash
git pull origin main
```