<template>
	<v-container>
    <v-row>
      <v-col cols="12" md="4" class="custom-margin-for-right">
				<v-btn @click="openFilePicker">
					<v-icon left>mdi-file-document</v-icon>
					開啟檔案
				</v-btn>
			</v-col>
			<v-col cols="12" md="8" class="custom-margin">
				<div
					class="drop-area"
					@dragover.prevent="handleDragOver"
					@drop.prevent="handleDrop"
				>
					或將檔案拖拽到這裡
				</div>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import * as XLSX from 'xlsx';

export default {
	name: 'FileUpLoader',

	methods: {
		openFilePicker() {
			const input = document.createElement('input');
			input.type = 'file';
			input.accept = '.xlsx'; // 僅接受 Excel 文件
			input.addEventListener('change', this.handleFileSelection);
			input.click();
		},

		handleFileSelection(event) {
			const file = event.target.files[0];
			if (file) {
				//const filePath = file.path; // 使用 file.path 獲取文件的本地路徑
				const fileName = file.name; // 獲取文件名稱
				console.log('Selected file name:', fileName);
				//console.log('Selected file path:', filePath);
				this.$emit('file-selected', fileName); // 發出自定義事件並將檔案名稱作為參數
				//this.readExcelFile(file);
			}
		},
		/*
		openFilePicker() {
			const input = document.createElement('input');
			input.type = 'file';
			input.accept = '.xlsx'; // Excel文件
			input.addEventListener('change', this.handleFile);
			input.click();
		},
		*/
		/*
		handleFile(event) {
			const file = event.target.files[0];
			if (file) {
				this.readExcelFile(file);
			}
		},

		handleFile(event) {
			const file = event.target.files[0];
			if (file) {
				console.log("file name: ", file.name)
				//this.$emit('file-selected', file.name); // 發出自定義事件並將檔案名稱作為參數
				//this.readExcelFile(file);
			}
		},
		*/
		/*
		handleFile(event) {
			const file = event.target.files[0];
			if (file) {
				const filePath = URL.createObjectURL(file); // 獲取檔案路徑
				console.log("file name: ", file.name);
				console.log("file path: ", filePath);
				//this.$emit('file-selected', { name: file.name, path: filePath }); // 發出自定義事件並將檔案名稱和路徑作為參數
				//this.readExcelFile(file);
			}
		},
		*/
		readExcelFile(file) {
			const reader = new FileReader();
			reader.onload = (e) => {
				const data = new Uint8Array(e.target.result);
				const workbook = XLSX.read(data, { type: 'array' });
				// 處理工作簿中的内容
				console.log(workbook);
			};
			reader.readAsArrayBuffer(file);
		},
		handleDragOver(event) {
			event.dataTransfer.dropEffect = 'copy';
		},
		handleDrop(event) {
			event.preventDefault();
			const file = event.dataTransfer.files[0];
			if (file) {
				this.readExcelFile(file);
			}
		},
	},
};
</script>

<style scoped>
.drop-area {
  border: 2px dashed #ccc;
  padding: 20px;
  text-align: center;
  cursor: pointer;
}

.drop-area-container {
  display: flex;
  align-items: center; /* 垂直居中 */
}

.drop-area {
  border: 2px dashed #ccc;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  width: 200px; /* 设置宽度 */
  height: 60px; /* 设置高度 */
}

.custom-margin {
  margin-left: 0px; /* 调整左侧间距，根据需要修改 */
	padding-left: 0px;
	position: relative;
  left: 20px;
}

.custom-margin-for-right {
  margin-right: 0px; /* 调整左侧间距，根据需要修改 */
	padding-right: 0px;
}
</style>