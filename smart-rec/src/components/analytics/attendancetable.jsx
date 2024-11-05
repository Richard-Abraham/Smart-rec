import Image from 'next/image';

export default function AttendanceTable({ records }) {
  return (
    <div className="mt-8 flow-root">
      <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <table className="min-w-full divide-y divide-gray-300">
            <thead>
              <tr>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Employee</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Date</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Check In</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Check Out</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {records.map((record) => (
                <tr key={record.id}>
                  <td className="whitespace-nowrap px-3 py-4">
                    <div className="flex items-center">
                      <Image className="h-10 w-10 rounded-full" src={record.user.photoUrl} alt="" />
                      <div className="ml-4">
                        <div className="font-medium text-gray-900">{record.user.name}</div>
                        <div className="text-gray-500">{record.user.department}</div>
                      </div>
                    </div>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{record.date}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{record.checkIn}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {record.checkOut || '-'}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm">
                    <span className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                      record.status === 'present'
                        ? 'bg-green-100 text-green-800'
                        : record.status === 'late'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {record.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
