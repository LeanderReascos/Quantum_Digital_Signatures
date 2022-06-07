# Quantum Digital Signatures

Leander Reascos

## Introdução

Foi demonstrado que com a existencia de computadores quanticos o suficientemente grandes em termos de qubits estaveis a criptografia asimetrica corre um grande risco. Isto vem do facto que como foi provado por Shor, os problemas que são dificieis para computadores classicos e nos quais se baseiam as tecnicas criptograficas assimetricas passam a ser facilmente resoluveis por computadores quanticos ao fazer uso do algoritmo de Shor e as suas variantes. 

Assim os problemas de fatorização e de logaritmo discreto são resolvidos em tempo util por computadores quanticas comprometendo todas as tecnicas criptograficas que façam usso deles. Neste contexto se encaixa as assinaturas digitais que funcionam por base a algoritmos de chave assimetrica como o RSA. 

De esta forma existe a necesidade do desenvolvimento de novas tecnicas criptograficas que garantam a segurança e as diferentes propriedades que são necesarias para a criptografia assimetrica. Assim foram propostas tecnicas *Post Quantum* e *Hibridas* que foram abordadas durante as aulas. Neste trabalho será abordada a técnica quântica, mais concretamente a assinatura quântica digtal *QDS (Quantum Digital Signatures)*.

Uma técnica criptografica quantica a diferença das tecnicas *Post Quantum* e *Hibridas*, requer que ambas das partes envolvidas na comunicação tenham acceso a dispositivos quânticos, portanto para o protocolo que vai ser estudado para *QDS* é necesario da existencia de um canal de comunicação autenticado quântico e um canal publico clasico.

Com o objetivo de mostrar o principio básico da tecnica das *QDS* vai ser estudado o protocolo proposto por Gottesman e Chuang em 2001 [[1]](/README.md#1-gottesman-daniel-and-chuang-isaac-quantum-digital-signatures-2001httpsarxivorgabsquant-ph0105032). Durante o proceso de investigação não foi encontrada informação relativa a experiencias deste protocolo fazendo uso de computadores quanticos ou simuladores unicamente com auxilio de laboratorios fotonicos [[2]](/README.md#2-roberts-gl-lucamarini-m-yuan-zl-et-al-experimental-measurement-device-independent-quantum-digital-signatures-nat-commun-8-1098-2017httpsdoiorg101038s41467-017-01245-5). Por tanto neste trabalho também é proposta uma simulação de um *QDS* para uma mensagem de um unico bit na qual se junta a teoria estudada ppor Gottesman e Chuang [[1]](/README.md#1-gottesman-daniel-and-chuang-isaac-quantum-digital-signatures-2001httpsarxivorgabsquant-ph0105032) e outros conceitos de computação quântica.

## Assinatura de Lamport

O protocolo de assinatura quantica digital proposto se baseia na assinatura classica de Lamport, onde de forma semelhante a todos os protocolos de criptografia assimetrica estudados gerá um par de chaves *(pk,sk)*. Por outro lado exige a existencia de uma função de sentido único *f* tal que *pk=f(sk)*.

Assim a assinatura da mensagem *m* é dada pela mensagem e pela chave privada *sk* *(m,yk=sk)* tal que a verificação da assinatura é *f(yk)=f(sk)=pk* o que implica que este par de chaves só pode ser usada uma unica vez, carateristica que é usada e assegurada pela fisica por tras de uma comunicação quântica.

A segurança desta assinatura é garantida pela função de sentido unico, impedindo a um adversario forjar uma uma chave para uma outra mensagem. 

## Protocolo de Gottesman e Chuang (GC-QDS)

O protocolo proposto se baseia no classico de Lamport, onde o par de chaves serem de uso unico é garantido pelas propriedades da fisica quantica. De esta forma é preciso a existencia de funções de sentido unico que no artigo discutido são propostas *Quantum Findgerprint*, *Stabilizer states* (Funções propostas para correção de erros) e o caso que vai ser discutido funções de Hash quantico que usam um unico qubit.

De esta forma o par de chaves consiste numa chave privada classica *sk* gerada aleartoriamente e uma chave publica quantica *|pk>* tal que é resultado da função de sentido unico quantica. Para a verificação dada as propriedades estocasticas que tem a computação quantica é necesaria a validação com varias copias das chaves publicas.

Assim dado o teorema da não clonagem o receitor não pode copiar os estados para a sua verificação, por tanto é trabalho do emisor criar diferentes "copias" dos estados quanticos que codificam a chave publica tanto para os diferentes elementos dentro da comunicação como para os receitores.

### Quantum Hashing

A função de sentido unico usada se baseia numa rotação a um qubit inicialmente no estado *|0>* dabase computacional. Tal que esta rotação é dada pela chave privada e pelo teorema de Holevo um adversario que tenha acceso a chave publica não pode ter acceso a mais do que *n* bits classicos a partir de *n* qubits assim se o numero de copias dos estados quanticos for limitado sendo *n* menor que o tamnanho das chaves um adversario não lhe é possivel conhecer a chave privada a partir da chave publica.

**|pk> = cos O |o> + sin O |1>**

**O = sk/N**, N: 2^L, L: Tamanho da chave privada

### Geração de Chaves

Com o explicado anteriormente é necesario que para uma unica mensagem, de um unico bit que é o caso em analise, exista um conjunto de chaves privadas e chaves publicas. Assim a chave privada é *SK={sk1, sk2, sk3, ...}* e a chave publica *PK={|pk1>, |pk2>, |pk3>, ...}*. Para este trabalho como se esta a explorar um protocolo quantico aproveitou-se das propriedades quanticas para que a geração de qualquer aleartoriedade seja produto de um estado em superposição uniforme quantico.

Para este caso de estudo só se tem em conta os participantes emisor, Alice e receitor, Bob, se existirem mais intervinientes na comunicação o numero de chaves a ser copiado por Alice incialmente aumenta, dada a necesidade de os outros participantes puderem validar a identidade de Alice e que esta esteja a ser honesta de forma a que as chaves publicas que recebem ambas das partes sejam iguais.

### Verificação

Para verificar a assinatura de uma mensagem de um unico bit a Alice tem de enviar ao Bob o par *(b,SKb)*, *b:{0,1}* e o Bob vai preparar os estados correspondetes as chaves privadas recebidas como assinaturas, consequentemente aplica o swap test para comparar a semelhança do seu estado preparado com o estado anteriormente recebido como chave publica por parte da Alice. Como foi referido dados os resultados probabilisticos o Bob precisa fazer isto para todo o conjunto de assinaturas (chaves privadas) e chaves publicas.

Os resultados do Swap test vão ser o estado *|0>* quando passa o test e ambos estados são iguais, e *|1>* com uma probabilidade não neglincenciavel se forem diferentes. No caso de se tratar de um dispositivo com ruido existe uma probabilidade extra de mesmo quando os estados serem iguais o swap test falahar. Por tanto para a verificação da assinatura quantica se introduzem certos valores de tolerancia para erros *c1* e *c2*.

- **c1*M:** Numero maximo de erros aceitaveis tal que a assinatura é valida.
- **c2*M:** Numero maximo de erros permitidos

Onde *M* é o numero total de chaves que contem cada grupo de chaves, desta forma a validez da assinatura parte da contagem de resultados de erros ao swap test para um dos estados *pki* que pertence a *PK* chamado de *r*, assim

- **1-ACC:** *r<c1M*. Quer dizer que o Bob aceita a assinatura como valida e que pelo menos mais uma pessoa a quem foi trasmitidas as chaves publicas de Alice vai aceitar a assinatura.
- **0-ACC:** *c1M<r<c2M*. O Bob aceita a assinatura mas mais nenhuma pessoa participante ira a aceitar a mesma como valida
- **REJ:** *r>c2M*. O Bob rejeita a assinatura

Estas respostas se devem ao facto de haver uma propriedade que precisam garantir as assinaturas e é que uma terceira parte possa validar o resultado que o Bob obteve denominado como um juri na literatura.

### Protocolo

Alice gera o conjunto de chaves *{SK0,SK1}* para a mensagem com o bit a 0 ou 1, e distribui as chaves publicas ao Bob, que no artigo é descrito como um procedimento que precisa o uso de acordo de chaves quantico *(QKD)*, isto no presente analise não foi tido em conta dado que se presupõe a existencia de um canal quantico seguro. Assim Bob recebe as chaves publicas *{PK0, PK1}* e as armazena até ser necesario a sua utilização, pelo que presupõe da existencia de uma memoria quantica sendo uma critica recorrente a esta tecnica. 

Posteriormente quando a Alice envia ao Bob a mensagem *b* e o seu correspondente conjunto de chaves privadas. Posteriormente o Bob aplica o algoritmo de verificação anteriormente descrito. Há que notar que a segurança de este protocolo se baseia novamente na existencia limitada de copias dos estados quanticos tal que um adversario nãp pode obter suficiente informação sobre a chave privada a partir da publica.

## Simulação do protocolo GC-QDS

Como referido anteriormente, toda escolha aleartoria é feita a partir de um circuito quantico em superposição uniforme de estados, assim o circuito que o representa é o seguinte

<img style="width:500px" src="Graficos/quantum_random.png">


## References

### [[1] Gottesman, Daniel and Chuang, Isaac. Quantum Digital Signatures. (2001).](https://arxiv.org/abs/quant-ph/0105032) 
### [[2] Roberts, G.L., Lucamarini, M., Yuan, Z.L. et al. Experimental measurement-device-independent quantum digital signatures. Nat Commun 8, 1098 (2017).](https://doi.org/10.1038/s41467-017-01245-5)