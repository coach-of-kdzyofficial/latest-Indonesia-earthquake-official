import requests
from bs4 import BeautifulSoup


def ekstraksi_data():
    """
    Tanggal: 22 November 2022, 19:22:27 WIB
    Magnitudo: 2.8
    Kedalaman: 2 km
    Lokasi: LS= 6.85 BT= 107.06
    Pusat Gempa: Pusat gempa berada di darat 9 km BaratDaya Cianjur
    Dirasakan: Dirasakan (Skala MMI): III Cugenang, III Cilaku
    :return:
    """
    try:
        content = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None

    if content.status_code == 200 :
        soup = BeautifulSoup(content.text, 'html.parser')
        tanggal = soup.find('span', {'class':'waktu'})
        result = tanggal.text.split(', ')
        tanggal = result[0]
        waktu = result[1]

        result = soup.find('div', {'class':'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')

        i=0
        magnitudo = None
        kedalaman = None
        koordinat = None
        lokasi = None
        ls = None
        bt = None
        dirasakan = None

        for res in result:
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split('-')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text
            i= i + 1

        hasil = dict()
        hasil['tanggal'] = tanggal #'22 November 2022'
        hasil['waktu'] = waktu #'19:22:27 WIB'
        hasil['magnitudo'] = magnitudo #2.8
        hasil['kedalaman'] = kedalaman #'2 km'
        hasil['koordinat'] = {'ls': ls, 'bt': bt}
        hasil['lokasi'] = lokasi #'Pusat gempa berada di darat 9 km BaratDaya Cianjur'
        hasil['dirasakan'] = dirasakan #'Dirasakan (Skala MMI): III Cugenang, III Cilaku'
        return hasil
    else:
        return None

def tampilkan_data(result):
    if result is None:
        print('Tidak Bisa Menemukan Data Gempa Terkini')
        return
    print('Gempa Terakhir Bersarkan BMKG')
    print(f"Tanggal {result['tanggal']}")
    print(f"Waktu {result['waktu']}")
    print(f"Magnitudo {result['magnitudo']}")
    print(f"Kedalaman {result['kedalaman']}")
    print(f"Koordinat: LS={result['koordinat']['ls']}, BT={result['koordinat']['bt']}")
    print(f"Lokasi {result['lokasi']}")
    print(f"Dirasakan {result['dirasakan']}")