from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random

class InstagramBot:

    def __init__(self,usuario,contraseña,driver_path,brave_path):

        self.usuario = usuario
        self.contraseña = contraseña
        self.driver_path = driver_path

        self.option = webdriver.ChromeOptions()
        self.option.binary_location = brave_path

        # driver
        self.r2d2 = webdriver.Chrome(executable_path=self.driver_path, chrome_options=self.option)
        sleep(3)

        self.r2d2.get("https://www.instagram.com/")
        sleep(5)

        # coloca el usuario
        username = self.r2d2.find_element_by_name("username")
        username.send_keys(self.usuario)
        username.send_keys(Keys.ENTER)
        sleep(3)

        # coloca la contraseña
        password = self.r2d2.find_element_by_name("password")
        password.send_keys(self.contraseña)
        password.send_keys(Keys.ENTER)
        sleep(3)

        # clickea el "Ahora no" de las notificaciones (el pop up), si no te aparece, borra esta linea o comentala.
        self.r2d2.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        sleep(3)

    # mientras mas cantidad de scrolls, se seguiran mas personas pero tambien es un riesgo
    # ya que instagram podria bloquear tu cuenta, por cada scroll, son mas o menos 10 seguidores.
    def seguir_seguidores(self,perfil, cantidad_de_scrolls):

        self.r2d2.get('https://www.instagram.com/'+perfil+'/')
        sleep(3)

        #abre la ventanilla de seguidores
        self.r2d2.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        sleep(3)

        for x in range(1,cantidad_de_scrolls + 1):
            try:

                # scrollea en la ventanilla de seguidores
                self.r2d2.execute_script('''
                    var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                    fDialog.scrollTop = fDialog.scrollHeight
                ''')
                sleep(3)

            except:
                continue

        hay_seguidores = True
        contador = 1
        while hay_seguidores:
            try:

                #sigue a todas las personas (una por una) encontradas despues del scroll
                self.r2d2.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li["+str(contador)+"]/div/div[2]/button").click()
                sleep(5)

                if contador == 1:
                    print("ya se siguio a :", contador, "persona")
                else:
                    print("ya se siguio a :", contador, "personas" )

                contador += 1

            except:
                print("- - - Ya se han seguido a todos los usuarios - - -")
                hay_seguidores = False

    # este metodo lo utilizo mas que nada en mi propio perfil para "limpiar"
    # algunos usuarios o mantener a mis seguidos en un numero bajo, asi como tambien
    # la utilizo despues de unas horas de seguir personas.
    # si no se cumple la cantidad de usuarios que quieres eliminar, en el primer for, 
    # aumentar el range "(1,6)"
    def dejar_de_seguir_usuarios(self,perfil, cant_usuarios):
        self.r2d2.get('https://www.instagram.com/'+perfil+'/')
        sleep(3)

        # abre la ventanilla de seguidos
        self.r2d2.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        sleep(3)

        for x in range(1,6):
            try:

                # scrollea en la ventanilla de seguidores
                self.r2d2.execute_script('''
                    var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                    fDialog.scrollTop = fDialog.scrollHeight
                ''')
                sleep(3)

            except:
                continue
    
        contador = 1
        while cant_usuarios != 0:
            try:
                self.r2d2.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li['+str(contador)+']/div/div[2]/button').click()
                sleep(3)

                self.r2d2.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
                sleep(5)
                
                cant_usuarios -= 1
                contador += 1

            except:
                continue
    
        print("- - - Ya se han dejado de seguir los usuarios - - -")
        print(contador-1, "usuarios eliminados")

    # recorre hashtags/hashtag, da likes y comenta
    # se recomienda que "numero_de_publicaciones" no exceda los 100 si es un solo hashtag, sino entre 20-30
    def recorrer_hashtags_likes_y_coments(self,hashtags_list, numero_de_publicaciones):

        hashtags = hashtags_list

        for elemento in hashtags:

            self.r2d2.get("https://www.instagram.com/explore/tags/"+elemento+"/")
            sleep(2)

            #abre la primera publicacion del hashtag
            self.r2d2.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]').click()
            sleep(5)

            rango = range(1,numero_de_publicaciones + 1)

            for x in rango: 
                
                #likear foto
                self.r2d2.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button').click()
                print("------Foto likeada------ : ", x)
                sleep(3)
                
                #comentar foto
                numeros = [0,1,2,3]
                numero_aleatorio = random.choice(numeros)
                
                self.r2d2.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[2]/button').click()
                sleep(3)
                comentario = self.r2d2.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                sleep(3)

                if numero_aleatorio == 0:
                    comentario.send_keys('Que lindoo! ;)')
                    print("------Comentario hecho------ : Que lindoo!;) ")
                    sleep(1)

                elif numero_aleatorio == 1:
                    comentario.send_keys('Me encantoo')
                    print("------Comentario hecho------ : Me encantoo ")
                    sleep(1)

                elif numero_aleatorio == 2:
                    comentario.send_keys(':D')
                    print("------Comentario hecho------ : :D ")
                    sleep(1)
                
                elif numero_aleatorio == 3:
                    comentario.send_keys(':)')
                    print("------Comentario hecho------ : :) ")
                    sleep(1)
            
                comentario.send_keys(Keys.ENTER)
                sleep(6)

                if x != numero_de_publicaciones:
                    self.r2d2.find_element_by_link_text('Siguiente').click()
                    sleep(10)
            
            print("Ya se likeo y comento el hashtag : " + elemento)
            print(" - - - - - - - - - - - - - - - - - - - - - - ")
            

if __name__ == "__main__":

    bot = InstagramBot("user","password","chromedriver.exe",
    ".exe")

    #bot.seguir_seguidores("user",amount)

    hashtags = [""]
    cantidad = 10
    bot.recorrer_hashtags_likes_y_coments(hashtags, cantidad)
    