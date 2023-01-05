import pygame, sys, random # Thêm thư viện pygame; sys hệ thống của máy, thêm vào để không còn hiện lỗi "video system ..."; thư viện ngẫu nhiên random

# CÁC HÀM
def draw_floor():
    screen.blit(floor,(floor_x_pos,650)) # (Hiện sàn lên của sổ) => Mỗi lần lặp, sàn hiện lên với một vị trí khác nhau (dịch trái 1), tạo cảm giác chym đang di chuyển
    screen.blit(floor,(floor_x_pos + 432,650)) # Tạo cái sàn thứ 2 kế tiếp ngay sau sàn thứ nhất (+432)
def create_pipe(): # Hàm để tạo ra ống
    random_pipe_pos = random.choice(pipe_height) # Chiều cao ống được lấy random trong danh sách pipe_height
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos)) # Tạo hcn xung quanh các ống để khi va chạm với con chim ta có thể nhận biết, midtop là vị trí hcn (ống) bát đầu xuất hiện trên cửa sỏ game (500, ngẫu nhiên)
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos-680)) # (ban đầu -650 không phải 680) Ống trên; -650 là khoảng cách ông trên ống dưới
    return bottom_pipe, top_pipe #
def move_pipe(pipes): # Hàm di chuyển những cái ống
    for pipe in pipes: # Vòng lặp những cái ống
        pipe.centerx -= 3 #(ban đầu -5) Lấy những ống vưà được tạo ra và di chuyển sang bên trái
    return pipes # Trả lại list những cái ống mới
def draw_pipe(pipes): # Hàm vẽ ống ra màn hình
    for pipe in pipes:
        if pipe.bottom >= 600: # Nếu chiều dài ống dưới >= chiều dài của sổ game thì: nó biết ống ở dưới
            screen.blit(pipe_surface,pipe) # pipe_surface là hình chèn vào
        else: # Trường hợp ngược lại là những ống ở trên
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) # pipe_surface là các ống, False là không lật theo trục x, True là lật theo trục y
            screen.blit(flip_pipe,pipe) # flip_pipe là ống đã dc lật
def check_collision(pipes): # Hàm xử lý va chạm
    for pipe in pipes:
        if bird_rect.colliderect(pipe): # Bird_rect là hình chữ nhật xung quanh con chym va chạm với cái ống thì
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650: # Hình chữ nhật xung quanh con chim có thể bay cao hơn cửa xổ game theo trục y một khoản -75 hoặc xuống dưới mặt sàn thì:
            return False
    return True
def rotate_bird(bird1): # Hàm xoay tạo hiệu ứng chim ngẩng lên ngẩng xuống
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*2,1) # rotozoom tạo hiệu ứng xoay, -bird_movement*2 để điều chỉnh mức độ xoay theo chiều chim chuyển động, 1 giữ nguyên kích thước hình ảnh
    return new_bird
def bird_animation(): # Hàm đập cánh cho chim
    new_bird = bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery)) # Tạo hcn mới xung quanh con chim, (100,ird_rect.centery) cách trục x 100 và nằm giữa trục y
    return new_bird, new_bird_rect
def score_display(game_state): # Hàm hiển thị điểm; thêm vào trạng thái của game là game_state
    if game_state == 'main game': # Có nghĩa là trò chơi đang hoạt động
    #    Thì hiển thị điểm khi game đang chạy
        score_surface = game_font.render(str(int(score)), True, (255,255,255)) # Biến hiển thị điểm theo font là game_font; render là xuất ra; 'Score' hiển thị chữ Score, (255,255,255) mã màu, str() chuyển vè dạng string; int() để ép về só nguyên do score += 0.01
        score_rect = score_surface.get_rect(center = (216,100)) # Tạo hcn cho ô chữ 
        screen.blit(score_surface, score_rect) # Hiển thị lên màn hình
    if game_state == 'game over': # Nếu trò chơi kết thúc
        # Hiển thị điểm ván vừa nãy
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255)) # Biến hiển thị điểm theo font là game_font; render là xuất ra; 'Score' hiển thị chữ Score, (255,255,255) mã màu, str() chuyển vè dạng string; int() để ép về só nguyên do score += 0.01
        score_rect = score_surface.get_rect(center = (216,100)) # Tạo hcn cho ô chữ 
        screen.blit(score_surface, score_rect) # Hiển thị lên màn hình
        # Hiển thị điểm cao nhất
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255)) # Biến hiển thị điểm theo font là game_font; render là xuất ra; 'Score' hiển thị chữ Score, (255,255,255) mã màu, str() chuyển vè dạng string; int() để ép về só nguyên do score += 0.01
        high_score_rect = high_score_surface.get_rect(center = (216,630)) # Tạo hcn cho ô chữ 
        screen.blit(high_score_surface, high_score_rect) # Hiển thị lên màn hình
def update_score(score, high_score): # Hàm cập nhật điểm cao nhất
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=512) # (frequency=44100,size=-16,channels=2,buffer=512) tham khảo trên web, nên thêm dòng lệnh này để âm thanh đúng thời gian thực, không còn trễ
pygame.init() # Mọi chương trình pygame đều bắt đầu bằng câu lệnh này

# Tạo cửa sổ pygame
# Tỉ lệ tùy thuộc vào hình ảnh background của game, như kích thước dưới là gấp đôi hình ảnh background đã tải về
screen = pygame.display.set_mode((432,768)) # Tạo dược cửa sổ pygame màu đen nháy lên rồi mất 
clock = pygame.time.Clock() # Tạo biến để cài đặt FPS trong pygame
game_font = pygame.font.Font('04B_19.ttf',40) # Tạo một biến load phông chữ của trò chơi: kiểu 04B_19.ttf; size 40
# Tạo các biến
gravity = 0.25 # Đặt biến trọng lực và gán giá trị, trọng lực được hiểu là làm con chim rơi xuống
bird_movement = 0 # =0 là do lúc đầu con chim chưa di chuyển
game_active = True # Biến này tể hiện trạng thái của game là đang hđ hay là kết thúc
score = 0 # Biến điểm bắt đầu bằng 0
high_score = 0 # Biến chứa điểm cao nhất
# Chèn background
bg = pygame.image.load('assets/background-night.png').convert() # Tạo 1 biến cho background là bg dc gán bằng ảnh background của game; .convert() để đổi file hình ảnh bằng 1 file nhẹ hơn để load nhanh hơn
bg = pygame.transform.scale2x(bg) # Làm hình backgrond của biến bg gấp đôi hình ban đầu
# Chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0 # Tọa độ sàn theo trục x
# Chèn chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up] # số thứ tự là 0 1 2; thay vì xuất 1 hình ảnh chim, ta xuất 3 hình ảnh chim để tạo hiệu ứng vỗ cánh
bird_index = 0
bird = bird_list[bird_index] # biến bird bắt đầu dc gán bằng biến bird_list[0] => hình ảnh chim bắt đầu xuất hiện từ biến ảnh này (bird_down)
#bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha() # Sửa convert thanhf convert_alpha để xóa màu đen của hcn xung quang con chim do rotozoom gây ra
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384)) #(ban đầu (100,384)) Tạo hình chữ nhật xung quanh con chim, đặt ở vị trí chính giữa của sỏ game (100, 384) 
# Tạo timer cho bird: 3 hình ảnh chim lần lượt dc xuất hiện theo tg
birdflap = pygame.USEREVENT+1 # Do trước đó ta đã dùng USEREVENT rồi nên +1 vào thể hiểu USEREVENT thứ 2
pygame.time.set_timer(birdflap,200) # 200ms
#  Chèn ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] # Tạo  list rỗng chứa những ống ta tạo ra
# Tạo timer: do các ống xuất hiện sau 1 khoảng tg nhất định
spawnpipe = pygame.USEREVENT # Là cho các ống xuất hiện liên tục
pygame.time.set_timer(spawnpipe, 1200) # Đặt một mốc tg; 1200 là sau 1.2 giây nó sẽ tạo một ống mới
pipe_height = [200,300,400] # tạo danh sách chiều dài ống, chiều dài ống random trong các giá trị này
# Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216, 384))
# Tạo biến âm thanh:
    # Tiếng đập cánh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav') # Tiếng đập cánh
    # Tiếng va chạm cột
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
    # Tiếng ghi điểm
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100 # đếm ngược bắt đầu từ 100
# Do màn hình chỉ hiện lên rồi tắt nên ta cần 1 vòng lặp cho nó hiện tắt rồi hiện tắt liên tục với mắt thường t sẽ thấy nó luôn hiện lên
# Trong game cũng có những vòng lặp sự kiện như: di chuyển chim hay va phải cột
while True: # Vòng lặp cho sự kiện (Với giá trị là True là đk lặp luôn là đúng nên vòng lặp cứ chạy mãi)
    for event in pygame.event.get(): # Lấy tấ cả sự kiện cảu pygame diễn ra
        if event.type == pygame.QUIT: # Sự kiện ấn vào để thoát cửa sổ game, nếu người chơi ấn phím thoát thì:
            pygame.quit() # Tắt cửa sổ game
            sys.exit() # Thoát hệ thống => Fix lỗi "video system ..."
        if event.type == pygame.KEYDOWN: # Thêm event tạo hiệu ứng trọng lực, khi có 1 phím nào trên máy tính dc ấn xuống:
            if event.key == pygame.K_SPACE and game_active: # Nếu bấm phím SPACE và game vẫn đang hđ
                bird_movement = 0 # Do trc đó ta mặc định tăng biến này là TH ta không ấn SPACE
                bird_movement =-6 #(ban đầu -11) giảm tọa độ trục y của con chim, cũng là độ dao động con chim nhảy lên nhảy xuống
                flap_sound.play() # Lệnh gọi ra tiếng 
            if event.key == pygame.K_SPACE and game_active == False: # Khi game đang không hoạt động và nhấn SPACE thì:
                 game_active = True # Game lại chạy trở lại
                 pipe_list.clear() # Reset lại những cái ống và con chim => xóa hết pipe_list đã dc tạo trong lúc chơi game lần trc
                 bird_rect.center = (100,384) # Đặt lại vị trí con chim
                 bird_movement = 0 # Chuyển động của con chim set lại =0
                 score = 0 # reset lại điểm khi trò chơi kết thúc
        if event.type == spawnpipe: # Sau 1.2 giây thì:
            pipe_list.extend(create_pipe()) # mỗi lần ống mới xuất hiện cần thêm vào list chưuá những ống đó # 
        if event.type == birdflap: # Lần lượt xuất hiện 3 hình ảnh cảu chim
            if bird_index < 2:
                bird_index += 1
            else: 
                bird_index = 0
            bird, bird_rect = bird_animation() # vẽ hình của chim và hình của rect lại do đã load 3 hình mới; hàm bird_animation() tạo ra hiệu ứng đập cánh


    screen.blit(bg,(0,0)) # Cú pháp thêm hình ảnh vào cửa sổ pygame, ở đây ta thêm hình ảnh background; (0,0) là tọa độ trên cùng bên trái của ảnh, x tăng sang phải, y tăng đi xuống
    if game_active: # Nếu game_active có giá trị True => game vẫn cần dc chạy tiếp =>  chim và ống vẫn hđ 
        # Chim
        bird_movement += gravity # Con chim càng di chuyển thì biến bird_movement càng tăng (theo trục y) => hiệu ứg trọng lực
        rotated_bird = rotate_bird(bird) # Hàm xoay hình ảnh chim tạo hiệu ứng chim ngẩng lên ngẩng xuống
        bird_rect.centery += bird_movement # Thay mỗi lần thay đổi tọa độ trục y của hcn bao quanh con chim cũng như tọa độ con chim => hiệu ứng con chim rơi xuống
        screen.blit(rotated_bird,bird_rect) # Hiển thị chim đã xoay lên cửa sổ, do đã tạo hcn xung quanh con chim nên phần tọa độ điền "bird_rect"
        game_active = check_collision(pipe_list) # Biến game_active được gán bởi giá trị rả về của hàm kiểm tra va chạm
        # Ống
        pipe_list = move_pipe(pipe_list) # Lấy tất cả những cái ống vừa dược tạo ra trong pipe_list để di chuyển sau đó trả lại pipe_list mới
        draw_pipe(pipe_list) # Vẽ ống ra màn hình, vẽ cho mình những list ống đang được tạo ra
        score += 0.01 # Điểm tự cộng theo thời gian
        score_display('main game') # Khi trò chơi hđ hiển thị điểm lên
        score_sound_countdown -= 1 # Giảm dần
        # Mỗi lần bay ghi dc 1 điểm nó sẽ có âm thanh ghi điểm
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    
    else: # Khi trò chơi két thúc
        high_score = update_score(score, high_score) # cập nhật điểm high_score
        score_display('game over') # Khi trò chơi kết thúc nó hiển thị điểm ván vừa kết thúc và điểm cao nhất
        screen.blit(game_over_surface, game_over_rect) 
    # Sàn
    floor_x_pos -= 1 # Mỗi lần lặp thì vị trí của sàn dịch sang trái 1, để tạo cảm giác con chim đang di chuyển theo chiều ngang trục x
    draw_floor() # Sau khi chạy hết 2 sàn thì hết, sàn không còn và không tạo cảm giác chim di chuyển nữa
    if floor_x_pos <= -432:
        floor_x_pos = 0 # Sau khi vị trí x của sàn thứ nhất ở -<=432 => đã chạy hết sàn 1 qua màn hình, sàn thứ 2 đứng ửo vị trí sàn 1 ban đầu => ta đưa sàn 1 vào ngay sau sàn thứ 2
    pygame.display.update() # Để hiển thị lên màn hình
    clock.tick(120) # (FPS =120) FPS càng cao tốc dộ game càng nhanh, để không quá nhanh và quá chậm thì cho FPS > 30

