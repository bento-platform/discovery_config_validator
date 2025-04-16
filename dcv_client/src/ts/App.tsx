import { Outlet, useLocation, useNavigate } from 'react-router';
import { Layout, Tabs, Typography } from 'antd';

const App = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Layout style={{ minHeight: '100vh', padding: 48 }}>
      <Layout.Content>
        <Typography.Title level={1} style={{ fontWeight: 'normal', textAlign: 'center' }}>
          <img
            src="/static/bento_logo.svg"
            alt="Bento"
            height={48}
            style={{ marginRight: '0.6em', verticalAlign: 'top' }}
          />
          Discovery Configuration Validator
        </Typography.Title>
        <div
          style={{
            backgroundColor: 'white',
            maxWidth: 1200,
            margin: '0 auto',
            padding: '0 24px 24px 24px',
            borderRadius: 12,
          }}
        >
          <Tabs
            size="large"
            defaultActiveKey={location.pathname.endsWith('schema') ? 'schema' : 'validate'}
            onChange={(k) => {
              navigate(k === 'schema' ? `/${k}` : '/');
            }}
            items={[
              { key: 'validate', label: 'Validate' },
              { key: 'schema', label: 'Schema' },
            ]}
          />
          <Outlet />
        </div>
      </Layout.Content>
    </Layout>
  );
};

export default App;
