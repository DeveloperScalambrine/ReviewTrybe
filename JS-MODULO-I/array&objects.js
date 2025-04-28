// // Faça um programa para adicionar pessoas clientes ao array do TrybeBank. A função deve se chamar addCustomer e receber um parâmetro do tipo string e, caso o parâmetro não seja do tipo string, retorne a mensagem: “O parâmetro passado deve ser do tipo string”.

// // const trybeBankCustomers = ['Oliva', 'Nat', 'Gus'];

// // function newCustomers(params) {
// //     let message = ''
// //     if (typeof params === "string") {
// //         trybeBankCustomers.push(params)
// //         console.log(`Customer ${params} add with success`);  
// //     } else {
// //         message = 'O parâmetro passado deve ser do tipo string'
// //         console.log(message)       
// //     }
// // }

// //     newCustomers('carlos');
// //     console.log(trybeBankCustomers);
    

// // const reader = {
// //     name: 'Julia',
// //     lastName: 'Pessoa',
// //     age: 21,
// //     favoriteBooks: [
// //       {
// //         title: 'O Senhor dos Anéis - a Sociedade do Anel',
// //         author: 'J. R. R. Tolkien',
// //         publisher: 'Martins Fontes',
// //       },
// //     ],
// //   };

// //   1 - Acesse as chaves name, lastName e title e exiba informações em um console.log() no seguinte formato: “O livro favorito de Julia Pessoa se chama ‘O Senhor dos Anéis - a Sociedade do Anel’.”.

// // const firstName = reader.name
// // const lastName = reader.lastName
// // const fullName = `${firstName} ${lastName}` 
// // const bookTitle = reader.favoriteBooks[0].title

// // console.log(`O livro favorito de ${fullName} se chama ${bookTitle}`)

// // 2 - Adicione um novo livro favorito na chave favoriteBooks, que é um array de objetos. Atribua a essa chave um objeto que contenha as seguintes informações:

// // reader.favoriteBooks.push({
// //     title: 'Harry Potter e o Prisioneiro de Azkaban',
// //     author: 'JK Rowling',
// //     publisher: 'Rocco',
// // })
// // console.log(`${reader.name} tem ${reader.favoriteBooks.length} livros favoritos`)


// // Imagine que você seja responsável por cuidar do sistema de entrega de um restaurante e que precise enviar mensagens com as informações da compra. Para isso, use o seguinte código:
// const order = {
//     name: 'Rafael Andrade',
//     phoneNumber: '11-98763-1416',
//     address: {
//       street: 'Rua das Flores',
//       number: '389',
//       apartment: '701',
//     },
//     order: {
//       pizza: {
//         marguerita: {
//           amount: 1,
//           price: 25,
//         },
//         pepperoni: {
//           amount: 1,
//           price: 20,
//         },
//       },
//       drinks: {
//         coke: {
//           type: 'Coca-Cola Zero',
//           price: 10,
//           amount: 1,
//         },
//       },
//       delivery: {
//         deliveryPerson: 'Ana Silveira',
//         price: 5,
//       },
//     },
//     payment: {
//       total: 60,
//     },
//   };
  
//   const customerInfo = (fullOrder) => {
//     fullOrder = (`Olá, ${order.order.delivery.deliveryPerson}, entrega para:
//     ${order.name}, Telefone: ${order.phoneNumber}, ${order.address.street}, Numero: ${order.address.number}, AP: ${order.address.apartment}`)
//     return fullOrder;
//   }
// //    console.log(customerInfo(order));
  
// //    const orderModifier = (fullOrder) => {
// //     const otherCustomer = order['name'] = "Luiz Silva"
// //     const newValue = order['payment'] = "50,00"
// //     fullOrder = (`Olá, ${order.name},  o valor total de seu pedido de marguerita, pepperoni e Coca-Cola Zero é R$ ${order.payment}`)       
// //     return fullOrder
// //    }
  
// //    console.log(orderModifier(order));



// // const addProperty = (object, key, value) => {
// //     if (typeof object[key] === "undefined"){
// //       object[key] = value;
// //     }
// //   };

// Suponha que você esteja trabalhando para uma escola e precise fazer algumas atualizações no sistema. Para isso, considere a seguinte base de dados:
// const school = {
//     lessons: [
//       {
//         course: 'Python',
//         students: 20,
//         professor: 'Carlos Patrício',
//         shift: 'Manhã',
//       },
//       {
//         course: 'Kotlin',
//         students: 10,
//         professor: 'Gabriel Oliva',
//         shift: 'Noite',
//       },
//       {
//         course: 'JavaScript',
//         students: 738,
//         professor: 'Gustavo Caetano',
//         shift: 'Tarde',
//       },
//       {
//         course: 'MongoDB',
//         students: 50,
//         shift: 'Noite',
//       },
//     ]
//   };

//   Crie uma função que obtenha o valor da chave de acordo com sua posição no array. Essa função deve possuir dois parâmetros: o objeto e a posição no array.

//   const getKey = (schoolObj, position) => {
//         if (!schoolObj.lessons || !Array.isArray(schoolObj.lessons)) {
//         return 'No array found in the object under "items"';
//     }
//         if (position < 0 || position >= schoolObj.lessons.length) {
//             return 'Position out of bounds';  
//         }

//         const lessons = schoolObj.lessons[position];
//         return Object.entries(lessons)
//   }

//   console.log(getKey(school, 1))

// Por meio do array de frutas chamado basket, crie um objeto que contenha o nome da fruta como chave e a quantidade de vezes que ela aparece no array como valor.
// Por exemplo, o array ['Melancia', 'Abacate', 'Melancia', 'Melancia', 'Uva'] deverá retornar:
// Em seguida, imprima esse resultado na tela com uma mensagem no seguinte formato: Sua cesta possui: x Melancias, x Abacates:
const basket = [
    'Melancia', 'Abacate', 'Melancia', 'Melancia', 'Uva', 'Laranja',
    'Jaca', 'Pera', 'Melancia', 'Uva', 'Laranja', 'Melancia',
    'Banana', 'Uva', 'Pera', 'Abacate', 'Laranja', 'Abacate',
    'Banana', 'Melancia', 'Laranja', 'Laranja', 'Jaca', 'Uva',
    'Banana', 'Uva', 'Laranja', 'Pera', 'Melancia', 'Uva',
    'Jaca', 'Banana', 'Pera', 'Abacate', 'Melancia', 'Melancia',
    'Laranja', 'Pera', 'Banana', 'Jaca', 'Laranja', 'Melancia',
    'Abacate', 'Abacate', 'Pera', 'Melancia', 'Banana', 'Banana',
    'Abacate', 'Uva', 'Laranja', 'Banana', 'Abacate', 'Uva',
    'Uva', 'Abacate', 'Abacate', 'Melancia', 'Uva', 'Jaca',
    'Uva', 'Banana', 'Abacate', 'Banana', 'Uva', 'Banana',
    'Laranja', 'Laranja', 'Jaca', 'Jaca', 'Abacate', 'Jaca',
    'Laranja', 'Melancia', 'Pera', 'Jaca', 'Melancia', 'Uva',
    'Abacate', 'Jaca', 'Jaca', 'Abacate', 'Uva', 'Laranja',
    'Pera', 'Melancia', 'Jaca', 'Pera', 'Laranja', 'Jaca',
    'Pera', 'Melancia', 'Jaca', 'Banana', 'Laranja', 'Jaca',
    'Banana', 'Pera', 'Abacate', 'Uva',
  ];

  const countFruits = (arr) => {
    const counts = {};

basket.forEach(fruit => {
  counts[fruit] = (counts[fruit] || 0) + 1;
});

const message = Object.entries(counts)
  .map(([fruit, qty]) => `${qty} ${fruit}${qty > 1 ? 's' : ''}`)
  .join(', ');

    console.log(`Sua cesta possui: ${message}`);
    return counts;
  }

countFruits(basket)