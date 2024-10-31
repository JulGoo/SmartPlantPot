# 식물 상태 진단 AI

### 데이터셋 정보
- 노지 작물 질병 진단 이미지 (AI HUB)   
https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=data&dataSetSn=147   
- 시설 작물 질병 진단 이미지 (AI HUB)
https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=153   


### 진행 내용
Docker로 제공되는 이미지를 실행하여 베스트 모델 추출   

- 노지 작물 질병 진단 Docker 이미지   
Docker : laonpeople/77_classification:v0.2   
- 시설 작물 질병 진단 Docker 이미지   
Docker : laonpeople/79_classification:v0.2   

<br>

추출한 두 가지의 모델을 Jupyter Notebook을 사용하여 정확도 확인
- openfiledModel.pt &nbsp;&nbsp; (노지 식물)
- houseplantModel.pt (시설 식물)

<br>

Anaconda 가상환경 생성 및 Jupyter Notebook Kernel 연결
```
conda create -n spp python=3.10
conda activate spp
pip install -r requirements.txt

conda deactivate
python -m ipykernel install --user --name spp --display-name "spp"
```

<br>

제공되는 모델파일에는 가중치 데이터만 포함되어 있기에, 데이터 설명서를 통해 RssNet-50 신경망을 사용중인것을 확인   
모델 평가 후 이미지를 넣어 분류 정확도 확인 예정




<br>

---
