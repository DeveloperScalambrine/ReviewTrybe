// // Helper function to apply multiple styles
// function applyStyles(element, styles) {
//     for (const [key, value] of Object.entries(styles)) {
//       element.style[key] = value;
//     }
//   }
  
//   // Create container for everything
//   const container = document.createElement('div');
//   applyStyles(container, {
//     fontFamily: 'Arial, sans-serif',
//     display: 'flex',
//     flexDirection: 'column',
//     alignItems: 'center',
//     minHeight: '100vh',
//     backgroundColor: '#0f3e30',
//     padding: '20px'
//   });
//   document.body.style.margin = '0';  // Remove body margin
//   document.body.appendChild(container);
  
//   // Header bar
//   const header = document.createElement('div');
//   header.textContent = 'Administrador do Tempo da Trybe';
//   applyStyles(header, {
//     backgroundColor: '#1eae56', // green top bar
//     color: 'white',
//     padding: '10px 0',
//     width: '600px',
//     textAlign: 'center',
//     fontWeight: 'bold',
//     fontSize: '18px',
//     borderRadius: '4px 4px 0 0'
//   });
//   container.appendChild(header);
  
//   // Main content area - grid container for 2x2 boxes
//   const mainGrid = document.createElement('div');
//   applyStyles(mainGrid, {
//     display: 'grid',
//     gridTemplateColumns: '1fr 1fr',
//     gridTemplateRows: '1fr 1fr',
//     width: '600px',
//     height: '300px',
//     border: '2px solid black',
//     borderRadius: '0 0 4px 4px',
//     boxSizing: 'border-box'
//   });
//   container.appendChild(mainGrid);
  
//   // Create each quadrant with appropriate background, label bar, and text content
  
//   // Common styles for labels
//   const labelStyle = {
//     height: '25px',
//     color: 'white',
//     fontWeight: 'bold',
//     fontSize: '14px',
//     lineHeight: '25px',
//     paddingLeft: '10px',
//     boxSizing: 'border-box'
//   };
  
//   // 1. Urgente e Importante (Top Left)
//   const box1 = document.createElement('div');
//   applyStyles(box1, { backgroundColor: '#f7a78b', position: 'relative' });
//   mainGrid.appendChild(box1);
  
//   const label1 = document.createElement('div');
//   label1.textContent = 'Urgente e Importante';
//   applyStyles(label1, { ...labelStyle, backgroundColor: 'purple' });
//   box1.appendChild(label1);
  
//   // 2. Não-Urgente e Importante (Top Right)
//   const box2 = document.createElement('div');
//   applyStyles(box2, { backgroundColor: '#f9de91', position: 'relative' });
//   mainGrid.appendChild(box2);
  
//   const label2 = document.createElement('div');
//   label2.textContent = 'Não-Urgente e Importante';
//   applyStyles(label2, { ...labelStyle, backgroundColor: 'black' });
//   box2.appendChild(label2);
  
//   // 3. Urgente e Não-Importante (Bottom Left)
//   const box3 = document.createElement('div');
//   applyStyles(box3, { backgroundColor: '#f7a78b', position: 'relative' });
//   mainGrid.appendChild(box3);
  
//   const label3 = document.createElement('div');
//   label3.textContent = 'Urgente e Não-Importante';
//   applyStyles(label3, { ...labelStyle, backgroundColor: 'purple' });
//   box3.appendChild(label3);
  
//   // 4. Não-Urgente e Não-Importante (Bottom Right)
//   const box4 = document.createElement('div');
//   applyStyles(box4, { backgroundColor: '#f9de91', position: 'relative' });
//   mainGrid.appendChild(box4);
  
//   const label4 = document.createElement('div');
//   label4.textContent = 'Não-Urgente e Não-Importante';
//   applyStyles(label4, { ...labelStyle, backgroundColor: 'black' });
//   box4.appendChild(label4);
  
//   // Footer
//   const footer = document.createElement('div');
//   footer.textContent = '© Trybe';
//   applyStyles(footer, {
//     marginTop: '20px',
//     color: 'white',
//     fontSize: '14px',
//     textAlign: 'center',
//     width: '600px'
//   });
//   container.appendChild(footer);

let parentItem = document.getElementById('parent')

let elementLi = document.createElement('li')

elementLi.innerHTML = "Create for DOM"

elementLi.appendChild(parentItem)



