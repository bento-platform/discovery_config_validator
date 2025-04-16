import { useEffect, useState } from 'react';
import JsonView from 'react18-json-view';
import { Skeleton } from 'antd';

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

  return isFetching ? (
    <Skeleton active={true} title={false} />
  ) : (
    <JsonView src={schema} enableClipboard={false} collapsed={2} />
  );
};

export default Schema;
