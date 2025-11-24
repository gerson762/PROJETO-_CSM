# 🎓 Educa Prime

**Educa Prime** é uma plataforma web para gestão educacional desenvolvida como projeto acadêmico. O sistema permite o gerenciamento de cursos, autenticação de usuários com diferentes perfis de acesso e apresentação institucional.

O projeto foi adaptado para rodar em ambiente **Serverless (Vercel)**, utilizando Python (Flask) no backend e JavaScript puro no frontend.

---

## 🚀 Funcionalidades

### 🔹 Área Pública
- **Página Institucional**: Informações sobre a empresa, missão e valores.
- **Catálogo de Cursos**: Visualização das formações oferecidas.
- **Páginas Informativas**: Contato, Apoio Pedagógico, RH, etc.
- **Políticas**: Termos de Uso e Política de Privacidade.

### 🔹 Área Administrativa (Sistema)
- **Autenticação**:
  - Login e Cadastro de novos usuários.
  - Recuperação de senha (Simulação de envio de token).
  - Controle de Sessão via LocalStorage.
- **Gestão de Cursos (CRUD)**:
  - Listagem de cursos disponíveis.
  - **Admin**: Pode Criar, Editar e Excluir cursos.
  - **Editor**: Pode apenas Editar cursos.
  - **Leitor**: Apenas visualização.
- **Segurança**:
  - Senhas criptografadas (Hash SHA-256).
  - Rotas protegidas por verificação de perfil no Backend.

---

## 🛠️ Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla/Puro).
- **Backend**: Python, Flask, Flask-Cors.
- **Banco de Dados**: Simulado em memória (Dicionários Python) para compatibilidade com Vercel Serverless.
- **Deploy**: Vercel.

---

## 🔐 Credenciais para Teste

Como o banco de dados é simulado e reinicia a cada deploy, utilize estas contas padrão para testar as funcionalidades:

| Perfil | E-mail | Senha | Permissões |
| :--- | :--- | :--- | :--- |
| **Admin** | `test@educaprime.com` | `senha123` | Criar, Editar, Excluir |
| **Leitor** | `leitor@educaprime.com` | `senha123` | Apenas Visualizar |

> **Nota:** Novos usuários cadastrados terão automaticamente o perfil de **Leitor**.

---


