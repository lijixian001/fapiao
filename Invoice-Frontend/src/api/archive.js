import request from '@/utils/request'

export function getArchiveList(params) {
  return request({
    url: '/invoice',
    method: 'get',
    params: { ...params, invoice_status: 4 }
  })
}
