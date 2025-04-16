import { useEffect, useState } from 'react';
import JsonView from 'react18-json-view';
import { Spin } from 'antd';

const fetchSchema = () => fetch('/api/v1/schema.json').then((res) => res.json());

const Schema = () => {
  const [schema, setSchema] = useState<object | null>(null);
  const [isFetching, setIsFetching] = useState<boolean>(false);

  useEffect(() => {
    setIsFetching(true);
    fetchSchema().then((schema) => {
      setSchema(schema);
      setIsFetching(false);
    });
  }, []);

  return (
    <Spin spinning={isFetching}>
      <JsonView src={schema} enableClipboard={false} collapsed={2} />
    </Spin>
  );
};

export default Schema;
