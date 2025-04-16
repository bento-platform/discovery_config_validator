import ReactDOM from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router';

import 'antd/dist/reset.css';
import 'react18-json-view/src/style.css';

import App from '@/App';
import Schema from '@/Schema';
import Validator from '@/Validator';

const RootApp = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />}>
        <Route index element={<Validator />} />
        <Route path="schema" element={<Schema />} />
      </Route>
    </Routes>
  </BrowserRouter>
);

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(<RootApp />);
