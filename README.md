# Live Camera Effects  
## Programa de manipulação de imagem da câmera utilizando multiplicações matriciais e transformações geométricas com foco em programação orientada a objetos para representação dos efeitos.

Developers:

* João Lucas de Moraes Barros Cadorniga [JoaoLucasMBC](https://github.com/JoaoLucasMBC)  
* Eduardo Mendes Vaz [EduardoMVaz](https://github.com/EduardoMVAz)

A ferramenta de manipulação de imagem acessa a câmera do computador e permite que o usuário rotacione ou expande a imagem utilizando o teclado.

---
<br/>

## Instalação e Utilização

Para utilizar o **live-camera-effects**, você deve ter Python instalado no seu computador e seguir os passos:

1. Clone o repositório na sua máquina na pasta de sua escolha. Utilize o comando:

`git clone https://github.com/JoaoLucasMBC/live-camera-effects.git`

2. Utilizando o terminal / a IDE de sua escolha, crie uma *Virtual Env* de Python e a ative:

`python -m venv env`

`env/Scripts/Activate.ps1` (Windows)

3. Mude para a pasta do programa e instale as bibliotecas requeridas:

`cd ./live-camera-effects`

`pip install -r requirements.txt`

4. Após a instalação, rode o arquivo `main.py` pelo terminal para testar o programa:

`python main.py`

Agora você pode começar a manipular a sua câmera com rotações!

---
<br/>

## Testando com `demo.py`

Caso o usuário deseje ver uma demonstração de todas as funcionalidades e efeitos do programa de maneira automática, basta rodar o arquivo `demo.py` e observar as seguintes transformações (você não precisa fazer nada!) seguindo o seguinte roteiro:

ROTEIRO

---
<br/>

## Modelo Matemático

Para realizar as transformações na imagem da câmera, o programa utiliza multiplicações matriciais para alterar cada pixel, e então os retorna transformados para serem renderizados na tela.

O frame da câmera, após ser capturado, é redimensionado para uma proporção 320x420 (visando diminuir o processamento computacional e aumentar a eficiência do programa), e, portanto, é gerada uma matriz de mesmas dimensões que representam os pixels da imagem.

A partir desse momento, os efeitos são aplicados por classes complementares que analisam o *input* do usuário (realizado pelo teclado e analisado pelos dicionários `commands` e `aux_commands`, da seguinte maneira:


### Comandos

* `r` - começa a rotação da imagem no sentido horário, com velocidade de 1°/frame  
* `t` - começa a rotação da imagem no sentido anti-horário, com velocidade de 1°/frame  
* `f` - progressivamente dobra a velocidade angular da rotação (não funciona no modo de controle manual)
* `w` - entra no modo de controle manual de rotação utilizando as teclas `a` e `d`, progredindo 5° por clique das teclas
* `e` e `c` - controlam a expansão e contração da imagem, respectivamente, em uma razão de dois. Ou o zoom dobra ou é diminuido em 50%  
* `x` - reseta todos os estados para a condição inicial
* `q` - encerra o programa e a utilização da câmera  

*obs: só é possível entrar no modo manual ou modo rotação quando o outro modo não está ativo. para desativar o modo atual, basta pressionar a tecla `x`*

<br/>

### Multiplicação Matricial

Todas as transformações são realizadas por classes auxiliares (`Rotation` e `Angle`), as quais possuem métodos estáticos que fazem multiplicações matriciais na matriz de imagem gerada. Após o processo, devolvem a nova imagem que será exibida na tela. 

*obs: o ângulo é iniciado em 0° e a velocidade angular em 1°/frame*

#### Rotation

Visando evitar o surgimento de artefatos e pixels vazios na imagem, a transformação é feita de maneira inversa: o progrema começa com uma matriz vazia de destino e utiliza as matrizes inversas das transformações para determinar os pixels da imagem original que devem "alimentar" os destinos. Por exemplo, a matriz de origem `X` de uma rotação é descoberta a partir da seguinte pré-multiplicação:  

$X = U^{-1} X_d$

Onde $U$ é a matriz de todas as transformações calculada como conjunto dos próximos passos.

A matriz de rotação R é determinada da seguinte maneira (exemplo de um ângulo de 45°):

$$
R = 
\begin{bmatrix}
    \cos(\theta) & -\sin(\theta) & 0 \\
    \cos(\theta) & \cos(\theta) & 0 \\
    0 & 0 & 1
\end{bmatrix} = 
\begin{bmatrix}
    \cos(45°) & -\sin(45°) & 0 \\
    \cos(45°) & \cos(45°) & 0 \\
    0 & 0 & 1
\end{bmatrix} = 
\begin{bmatrix}
    0.7 & -0.7 & 0 \\
    0.7 & 0.7 & 0 \\
    0 & 0 & 1
\end{bmatrix}
$$
<br/>

Para o redimensionamento da imagem, dobrando (Zoom In) ou dividindo por dois (Zoom Out) o tamanho, a matriz respectiva é selecionada pelo input do usuário:

* Zoom In: 

$$
E = \begin{bmatrix}
    2 & 0 & 0\\
    0 & 2 & 0 \\
    0 & 0 & 1
\end{bmatrix}
$$

* Zoom Out: 

$$
E = \begin{bmatrix}
    0.5 & 0 & 0\\
    0 & 0.5 & 0 \\
    0 & 0 & 1
\end{bmatrix}
$$

Ademais, como as transformações são centradas na **origem** do sistema de coordenadas, que está na borda, antes delas serem realizadas é preciso transportar a imagem para a origem, utilizando a seguinte matriz $T$:

$$
T = \begin{bmatrix}
    1 & 0 & -\Delta x \\
    0 & 1 & -\Delta y \\
    0 & 0 & 1
\end{bmatrix}
$$ 

Onde as variações são menos as dimensões da imagem divididos por 2, para que o centro seja movido. 

E, ao fim da transformação, o centro da imagem é transladado de volta por $T_2$:

$$
T2 = \begin{bmatrix}
    1 & 0 & \Delta x \\
    0 & 1 & \Delta y \\
    0 & 0 & 1
\end{bmatrix}
$$

Portanto, a matriz de origem é determinada utilizando as matrizes inversas das transformações aplicadas no destino `Xd`:

$U = T_2 R E T$

$X = U^{-1} X_d$

Finalmente, essa matriz `X` de coordenadas representa de onde saem os pixels que acabam nas coordenadas `Xd` da imagem final, que é renderizada na tela.

*OBS: além disso, são aplicados filtros para tratamento dos pixels:*

1. Todos os valores dos pixels são transformados para `float`, já que a transformação pode retornar valores decimais.  
2. São filtrados os pixels que cairíam foram do enquadramento de 320x240 antes de passar os pixels da imagem original para o novo array. 

#### Angle

A classe `Angle` realiza a manipulação do ângulo de rotação a cada loop do programa, de acordo com os comandos do teclado do usuário e um dicionário de `ESTADOS` que organiza qual o tipo de rotação (constante ou manual) a direção (normal ou reversa) e o incremento (velocidade angular) da rotação. 

Além disso, o método `restart` retorna todos os parâmetros para as condições iniciais:

* `rotate = False` (parado)  
* `reverse` = False` (direção horária)  
* `wasd = False` (não está no modo manual)  
* `incremento = 1` (velocidade angular de 1°/frame)
* `angle = 0` (retorna para o ângulo inicial)
