/**
 * 縣市鄉鎮聯動下拉式選單
 * 適用於案件表單和個人資料表單
 */

class CityTownshipSelector {
  constructor(citySelectId, townshipSelectId, options = {}) {
    this.citySelect = document.getElementById(citySelectId);
    this.townshipSelect = document.getElementById(townshipSelectId);
    this.options = {
      cityPlaceholder: '請選擇縣市',
      townshipPlaceholder: '請選擇鄉鎮',
      apiUrl: options.apiUrl || '/api/townships/',
      ...options,
    };

    // 儲存初始的鄉鎮值
    this.initialTownshipName = this.townshipSelect.value;

    // 如果有隱藏的初始鄉鎮值，使用它
    const hiddenTownship = document.getElementById('initial_township');
    if (hiddenTownship) {
      this.initialTownshipName = hiddenTownship.value;
    }

    // 如果是個人資料表單，檢查是否有隱藏的初始鄉鎮值
    const hiddenUserTownship = document.getElementById('initial_user_township');
    if (hiddenUserTownship) {
      this.initialTownshipName = hiddenUserTownship.value;
    }

    this.init();
  }

  init() {
    if (!this.citySelect || !this.townshipSelect) {
      console.error('CityTownshipSelector: 找不到指定的select元素');
      return;
    }

    // 綁定縣市變更事件
    this.citySelect.addEventListener('change', () => {
      this.updateTownships();
    });

    // 初始化鄉鎮選項
    this.updateTownships();
  }

  updateTownships() {
    const cityName = this.citySelect.value;

    // 清空鄉鎮選項
    this.townshipSelect.innerHTML = '';
    this.townshipSelect.appendChild(
      this.createOption('', this.options.townshipPlaceholder),
    );

    if (!cityName) {
      return;
    }

    // 發送AJAX請求獲取鄉鎮資料
    fetch(`${this.options.apiUrl}?city_id=${encodeURIComponent(cityName)}`)
      .then((response) => response.json())
      .then((data) => {
        data.forEach((township) => {
          const option = this.createOption(township.id, township.name);
          this.townshipSelect.appendChild(option);
        });

        // 如果有初始鄉鎮值，嘗試設定它
        if (this.initialTownshipName) {
          this.townshipSelect.value = this.initialTownshipName;
        }
      })
      .catch((error) => {
        console.error('獲取鄉鎮資料失敗:', error);
      });
  }

  createOption(value, text) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = text;
    return option;
  }

  // 設定初始值
  setInitialValues(cityName, townshipName) {
    if (cityName) {
      this.citySelect.value = cityName;
      this.updateTownships();

      // 等待鄉鎮選項載入完成後設定鄉鎮值
      setTimeout(() => {
        if (townshipName) {
          this.townshipSelect.value = townshipName;
        }
      }, 200);
    }
  }

  // 獲取選中的值
  getSelectedValues() {
    return {
      cityName: this.citySelect.value,
      cityDisplayName:
        this.citySelect.options[this.citySelect.selectedIndex]?.text || '',
      townshipName: this.townshipSelect.value,
      townshipDisplayName:
        this.townshipSelect.options[this.townshipSelect.selectedIndex]?.text ||
        '',
    };
  }

  // 清空選擇
  clear() {
    this.citySelect.value = '';
    this.townshipSelect.innerHTML = '';
    this.townshipSelect.appendChild(
      this.createOption('', this.options.townshipPlaceholder),
    );
  }
}

// 當DOM載入完成後，如果有初始值，設定它們
document.addEventListener('DOMContentLoaded', function () {
  // 檢查是否在案件表單頁面
  const caseCitySelect = document.getElementById('id_yfcaseCity');
  const caseTownshipSelect = document.getElementById('id_yfcaseTownship');

  if (caseCitySelect && caseTownshipSelect && window.caseCityTownshipSelector) {
    // 如果有初始值，設定它們
    const initialCityName = caseCitySelect.value;
    const initialTownshipName = caseTownshipSelect.value;

    if (initialCityName) {
      // 延遲執行，確保選擇器已經初始化
      setTimeout(() => {
        window.caseCityTownshipSelector.setInitialValues(
          initialCityName,
          initialTownshipName,
        );
      }, 100);
    }
  }

  // 檢查是否在個人資料頁面
  const userCountrySelect = document.getElementById('id_userCountry');
  const userTownshipSelect = document.getElementById('id_userTownship');

  if (
    userCountrySelect &&
    userTownshipSelect &&
    window.userCityTownshipSelector
  ) {
    // 如果有初始值，設定它們
    const initialCountryName = userCountrySelect.value;
    const initialTownshipName = userTownshipSelect.value;

    if (initialCountryName) {
      // 延遲執行，確保選擇器已經初始化
      setTimeout(() => {
        window.userCityTownshipSelector.setInitialValues(
          initialCountryName,
          initialTownshipName,
        );
      }, 100);
    }
  }
});
