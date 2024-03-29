original_url_list = []
slug_list = []


# DB에서 반환한 index를 Base62로 인코딩 하는 함수
def base62(index):
	result = ""
	# Base62 인코딩의 기본이 되는 문자들(배열은 상관없이 중복이 없으면 됩니다.)
	words = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

	while index % 62 > 0 or result == "": # index가 62인 경우에도 적용되기 위해 do-while 형식이 되도록 구현했다.
		result = result + words[index % 62]
		index = int(index / 62)

	return result

# URL을 단축 URL로 만드는 함수
def Generate(URL):
	# DB에 URL Insert
	index = original_url_list.index(URL)
	# URL이 등록 된 Index를 Base62로 인코딩
	short_slug = base62(index)
 
	return short_slug


# 출처: https://blog.siyeol.com/26 [Kent's Diary:티스토리]

def generate_slug(url):
    # url을 리스트에 추가, 리스트의 인덱스로 슬러그 생성 후 슬러그를 리스트에 추가
    
    original_url_list.append(url)
    slug = Generate(url)
    slug_list.append(slug)
    
    return slug

def search_slug(short_slug):
    for index in range(len(slug_list)):
        if slug_list[index] == short_slug:
            return index
    return -1

def get_slug(index):
    return slug_list[index]

def search_url(url):
    for index in range(len(original_url_list)):
        if original_url_list[index] == url:
            return index
    return -1

def get_url(index):
    return original_url_list[index]