import './main.css';
import { createRoot } from 'react-dom/client';

import { Root } from './app/router/Root';
import { Provider } from 'react-redux';
import store from './app/store/store';
import { AuthLoader } from './components/authLoader/authLoader';



createRoot(document.getElementById('root') as HTMLElement).render(
  <Provider store={store}>
    <AuthLoader>
      <Root />
      </AuthLoader>
  </Provider>);
